"""Exchange an explicitly approved device request for a regular HA session."""

from __future__ import annotations

from dataclasses import dataclass
from hmac import compare_digest
import re
import secrets
from time import monotonic, time

from aiohttp import web
from homeassistant.auth import InvalidAuthError, InvalidProvider
from homeassistant.auth.models import TOKEN_TYPE_NORMAL, User
from homeassistant.components.http import HomeAssistantView
from homeassistant.components.http.const import KEY_HASS_REFRESH_TOKEN_ID
from homeassistant.core import HomeAssistant
from yarl import URL

try:
    from homeassistant.components.http.auth_util import async_user_not_allowed_do_auth
except ImportError:
    from homeassistant.components.http.auth import async_user_not_allowed_do_auth

from ..application.services import PwaAppService
from ..const import API_BASE_PATH, HTTP_BASE_PATH

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
_LIFETIME = 300
_REFERENCE_PATTERN = re.compile(r"[A-Za-z0-9_-]{24}")


@dataclass
class PairingRequest:
    app_id: str
    slug: str
    origin: str
    address: str | None
    secret: str
    reference: str
    expires_at: float
    approval: tuple[str, str] | None = None


class PairingRequests:
    """Keep a bounded, temporary record for each device awaiting approval."""

    def __init__(self, apps: PwaAppService) -> None:
        self.apps = apps
        self.pending: dict[str, PairingRequest] = {}
        self.active = False

    def get(self, code: str) -> PairingRequest | None:
        pairing = self.pending.get(code)
        if pairing and pairing.expires_at <= monotonic():
            self.pending.pop(code)
            return None
        return pairing if self.active else None

    def code_for_reference(self, reference: str) -> str | None:
        return next((code for code, req in self.pending.items() if req.reference == reference), None)

    def create(self, app_id: str, slug: str, origin: str, address: str | None) -> tuple[str, PairingRequest]:
        now = monotonic()
        self.pending = {code: req for code, req in self.pending.items() if req.expires_at > now}
        if len(self.pending) >= 128 or sum(req.address == address for req in self.pending.values()) >= 12:
            raise web.HTTPTooManyRequests()
        code = "".join(secrets.choice(_ALPHABET) for _ in range(12))
        while code in self.pending:
            code = "".join(secrets.choice(_ALPHABET) for _ in range(12))
        pairing = PairingRequest(
            app_id, slug, origin, address, secrets.token_urlsafe(32), secrets.token_urlsafe(18),
            now + _LIFETIME,
        )
        self.pending[code] = pairing
        return code, pairing

    def allowed_app(self, pairing: PairingRequest, user: User):
        app = self.apps.get_app(pairing.app_id)
        if (self.active and app and app.slug == pairing.slug and app.access.allow_companion_pairing
                and not user.system_generated
                and self.apps.can_user_access(app, user.id, user.is_admin, user.local_only)):
            return app
        return None


def _reply(data: dict, status: int = 200) -> web.Response:
    return web.json_response(data, status=status, headers={"Cache-Control": "no-store"})


async def _read_body(request: web.Request) -> tuple[str, dict]:
    origin = f"{request.scheme}://{request.host}"
    if (request.headers.get("Origin") != origin
            or (request.scheme != "https" and URL(origin).host not in ("localhost", "127.0.0.1", "::1"))):
        raise web.HTTPForbidden()
    if request.content_type != "application/json" or not 0 < (request.content_length or 0) <= 1024:
        raise web.HTTPBadRequest()
    try:
        body = await request.json()
    except ValueError as err:
        raise web.HTTPBadRequest() from err
    if not isinstance(body, dict):
        raise web.HTTPBadRequest()
    return origin, body


def _code(body: dict) -> str:
    code = body.get("code")
    if not isinstance(code, str) or len(code) != 12 or any(ch not in _ALPHABET for ch in code):
        raise web.HTTPBadRequest()
    return code


class CompanionPairingView(HomeAssistantView):
    """Start a device request and redeem it using the private device proof."""

    url = f"{API_BASE_PATH}/companion/device/{{slug}}"
    name = "pwa_app_studio:companion_device"
    requires_auth = False

    def __init__(self, hass: HomeAssistant, requests: PairingRequests) -> None:
        self._hass = hass
        self._requests = requests

    async def post(self, request: web.Request, slug: str) -> web.Response:
        origin, body = await _read_body(request)
        app = self._requests.apps.get_app_by_slug(slug)
        if not self._requests.active or not app or not app.access.allow_companion_pairing:
            raise web.HTTPNotFound()
        if not body:
            code, pairing = self._requests.create(app.app_id, app.slug, origin, request.remote)
            return _reply({
                "code": code, "secret": pairing.secret, "reference": pairing.reference,
                "expires_in": _LIFETIME,
            }, 201)

        code = _code(body)
        pairing = self._requests.get(code)
        secret = body.get("secret")
        if (not pairing or pairing.app_id != app.app_id or pairing.slug != app.slug
                or pairing.origin != origin or not isinstance(secret, str) or not secret.isascii()
                or not compare_digest(pairing.secret, secret)):
            raise web.HTTPNotFound()
        if not pairing.approval:
            return _reply({"state": "pending"}, 202)

        # Consume the grant before the first await, including during concurrent redemption.
        self._requests.pending.pop(code)
        user_id, source_id = pairing.approval
        user = await self._hass.auth.async_get_user(user_id)
        source = user.refresh_tokens.get(source_id) if user else None
        if (not source or not source.credential or not self._requests.allowed_app(pairing, user)
                or async_user_not_allowed_do_auth(self._hass, user, request)
                or (getattr(source, "expire_at", None) is not None and source.expire_at <= time())):
            raise web.HTTPForbidden()
        try:
            self._hass.auth.async_validate_refresh_token(source, request.remote)
        except (InvalidAuthError, InvalidProvider) as err:
            raise web.HTTPForbidden() from err

        client_id = f"{origin}{HTTP_BASE_PATH}/app/{app.slug}/client"
        token = await self._hass.auth.async_create_refresh_token(
            user, client_id, client_name="PWA Web-App Studio", credential=source.credential,
        )
        try:
            if (source_id not in user.refresh_tokens or not self._requests.allowed_app(pairing, user)
                    or async_user_not_allowed_do_auth(self._hass, user, request)):
                raise InvalidAuthError("Device approval is no longer valid")
            access_token = self._hass.auth.async_create_access_token(token, request.remote)
        except (InvalidAuthError, InvalidProvider) as err:
            await self._hass.auth.async_remove_refresh_token(token)
            raise web.HTTPForbidden() from err
        return _reply({
            "access_token": access_token,
            "refresh_token": token.token,
            "expires_in": int(token.access_token_expiration.total_seconds()),
            "token_type": "Bearer",
            "ha_auth_provider": source.credential.auth_provider_type,
        })


class CompanionApprovalView(HomeAssistantView):
    """Show and approve a device request from an authenticated HA frontend."""

    url = f"{API_BASE_PATH}/companion/approve"
    name = "pwa_app_studio:companion_approve"
    requires_auth = True

    def __init__(self, hass: HomeAssistant, requests: PairingRequests) -> None:
        self._hass = hass
        self._requests = requests

    async def post(self, request: web.Request) -> web.Response:
        _, body = await _read_body(request)
        if "reference" in body:
            reference = body["reference"]
            if not isinstance(reference, str) or not _REFERENCE_PATTERN.fullmatch(reference):
                raise web.HTTPBadRequest()
            code = self._requests.code_for_reference(reference)
            if not code:
                raise web.HTTPNotFound()
            if body.get("confirm") is True and _code(body) != code:
                raise web.HTTPBadRequest()
        else:
            code = _code(body)
        pairing = self._requests.get(code)
        if not pairing or pairing.approval:
            raise web.HTTPNotFound()
        user = request["hass_user"]
        source_id = request.get(KEY_HASS_REFRESH_TOKEN_ID)
        source = user.refresh_tokens.get(source_id)
        app = self._requests.allowed_app(pairing, user)
        if (not app or not source or source.token_type != TOKEN_TYPE_NORMAL or not source.credential
                or async_user_not_allowed_do_auth(self._hass, user, request)):
            raise web.HTTPForbidden()
        if body.get("confirm") is True:
            pairing.approval = (user.id, source_id)
            return _reply({"state": "approved"})
        return _reply({
            "name": app.manifest.name, "origin": pairing.origin, "account": user.name, "code": code,
        })
