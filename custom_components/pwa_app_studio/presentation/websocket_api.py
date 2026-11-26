'''WebSocket commands for PWA App Studio (Admin CRUD + ACL-checked runtime).'''

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.network import get_url

from ..application.services import DistributionService, PwaAppService
from ..const import DOMAIN
from ..infrastructure.lovelace_adapter import HaLovelaceAdapter, HaUserDirectoryAdapter


def async_register_websocket_commands(
    hass: HomeAssistant,
    app_service: PwaAppService,
    distribution_service: DistributionService,
    lovelace_adapter: HaLovelaceAdapter,
    user_directory: HaUserDirectoryAdapter,
) -> None:
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/apps/list"})
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_list_apps(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        apps = [app.to_dict() for app in app_service.list_apps()]
        connection.send_result(msg["id"], {"apps": apps})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/apps/create",
            vol.Required("payload"): dict,
        }
    )
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_create_app(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        try:
            app = await app_service.async_create_app(msg["payload"])
            connection.send_result(msg["id"], {"app": app.to_dict()})
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_format", str(err))

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/apps/update",
            vol.Required("app_id"): str,
            vol.Required("payload"): dict,
        }
    )
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_update_app(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        try:
            app = await app_service.async_update_app(msg["app_id"], msg["payload"])
            connection.send_result(msg["id"], {"app": app.to_dict()})
        except KeyError as err:
            connection.send_error(msg["id"], "not_found", str(err))
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_format", str(err))

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/apps/delete",
            vol.Required("app_id"): str,
        }
    )
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_delete_app(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        deleted = await app_service.async_delete_app(msg["app_id"])
        if not deleted:
            connection.send_error(msg["id"], "not_found", "PWA app not found.")
            return
        connection.send_result(msg["id"], {"deleted": True})

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/lovelace/list"})
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_list_lovelace(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        dashboards = await lovelace_adapter.async_list_dashboards()
        connection.send_result(msg["id"], {"dashboards": dashboards})

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/users/list"})
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_list_users(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        users = await user_directory.async_list_registered_users()
        connection.send_result(msg["id"], {"users": users})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/qr/generate",
            vol.Required("app_id"): str,
            vol.Optional("origin"): str,
        }
    )
    @websocket_api.require_admin
    @websocket_api.async_response
    async def ws_generate_qr(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        app = app_service.get_app(msg["app_id"])
        if app is None:
            connection.send_error(msg["id"], "not_found", "PWA app not found.")
            return
        origin = msg.get("origin")
        if not origin:
            try:
                origin = get_url(hass, allow_internal=True)
            except Exception:  # noqa: BLE001
                origin = ""
        info = await distribution_service.async_build_distribution_info(app, origin)
        connection.send_result(msg["id"], info)

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/runtime/get",
            vol.Required("slug"): str,
        }
    )
    @websocket_api.async_response
    async def ws_runtime_get(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        app = app_service.get_app_by_slug(msg["slug"])
        if app is None:
            connection.send_error(msg["id"], "not_found", "PWA app not found.")
            return
        user = connection.user
        if not user.is_active or not app_service.can_user_access(app, user.id, user.is_admin):
            connection.send_error(
                msg["id"],
                "unauthorized",
                "Dieser Benutzer besitzt keine Berechtigung für diese PWA.",
            )
            return
        connection.send_result(
            msg["id"],
            {
                "app_id": app.app_id,
                "slug": app.slug,
                "version": app.version,
                "manifest": app.manifest.to_dict(),
                "content": app.content.to_dict(),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "is_admin": user.is_admin,
                },
            },
        )

    @callback
    def _register_all() -> None:
        websocket_api.async_register_command(hass, ws_list_apps)
        websocket_api.async_register_command(hass, ws_create_app)
        websocket_api.async_register_command(hass, ws_update_app)
        websocket_api.async_register_command(hass, ws_delete_app)
        websocket_api.async_register_command(hass, ws_list_lovelace)
        websocket_api.async_register_command(hass, ws_list_users)
        websocket_api.async_register_command(hass, ws_generate_qr)
        websocket_api.async_register_command(hass, ws_runtime_get)

    _register_all()
