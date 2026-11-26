"""The integration inside a genuine Home Assistant core.

They need Home Assistant and pytest-homeassistant-custom-component. The shared
engine installs both for every release the Compatibility workflow lists; to run them
locally: python .engine/.scripts/ha_matrix.py run 2026.9.4
"""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
from xml.etree import ElementTree

import pytest
from aiohttp.test_utils import make_mocked_request

pytest.importorskip("pytest_homeassistant_custom_component")

from homeassistant.components import http  # noqa: E402
from homeassistant.config_entries import ConfigEntryState  # noqa: E402
from homeassistant.setup import async_setup_component  # noqa: E402
from pytest_homeassistant_custom_component.common import MockConfigEntry  # noqa: E402

DOMAIN = next((Path(__file__).resolve().parents[2] / "custom_components").iterdir()).name


@pytest.fixture(autouse=True)
async def _real_home_assistant(verify_cleanup, enable_custom_integrations, hass, monkeypatch):
    """Load real frontend dependencies instead of marking them as loaded."""
    monkeypatch.setattr(http.HomeAssistantHTTP, "start", AsyncMock())
    monkeypatch.setattr(http.HomeAssistantHTTP, "stop", AsyncMock())
    if hasattr(http.HomeAssistantHTTP, "async_bind"):
        monkeypatch.setattr(http.HomeAssistantHTTP, "async_bind", AsyncMock())
    if hasattr(http, "async_get_source_ip"):
        monkeypatch.setattr(http, "async_get_source_ip", AsyncMock(return_value="127.0.0.1"))
    # Legacy onboarding imports recorder through analytics. Load the actual HTTP,
    # frontend and Lovelace paths without starting this unrelated telemetry stack.
    hass.config.components.add("analytics")
    assert await async_setup_component(hass, "panel_custom", {})
    assert await async_setup_component(hass, "lovelace", {})


async def test_user_flow_creates_the_single_entry_and_refuses_a_second(hass):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    assert result["type"] == "form"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["type"] == "create_entry"
    await hass.async_block_till_done()
    again = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    assert again["type"] == "abort" and again["reason"] == "single_instance_allowed"


async def test_entry_loads_and_unloads(hass):
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    assert any("pwa" in state.entity_id for state in hass.states.async_all("button"))
    assert await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_sidebar_option_reloads_panel(hass):
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    panels = hass.data["frontend_panels"]
    assert panels["pwa-app-studio"].sidebar_title == "PWA Web-App Studio"
    flow = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        flow["flow_id"], {"show_in_sidebar": False}
    )
    assert result["type"] == "create_entry"
    await hass.async_block_till_done()
    assert panels["pwa-app-studio"].sidebar_title is None
    assert "pwa-app-studio-runner" in panels


@pytest.fixture
async def studio(hass):
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    return hass.data[DOMAIN]["runtime"].app_service


async def test_guest_runtime_requires_selected_active_local_account(studio):
    from custom_components.pwa_app_studio.presentation.http_views import PwaRuntimeApiView

    app = await studio.async_create_app({
        "slug": "terrasse",
        "access": {"local_guests": True, "allowed_user_ids": ["gast"]},
    })
    view = PwaRuntimeApiView(studio)
    for user_id, local_only, active, admin, expected in [
        ("gast", True, True, False, 200),
        ("gast", False, True, False, 403),
        ("gast", True, False, False, 403),
        ("fremd", True, True, False, 403),
        ("verwaltung", False, True, True, 200),
    ]:
        user = SimpleNamespace(
            id=user_id, name=user_id, local_only=local_only, is_active=active, is_admin=admin,
        )
        response = await view.get({"hass_user": user}, app.slug)
        assert response.status == expected


async def test_failed_storage_does_not_change_live_app(studio, monkeypatch):
    app = await studio.async_create_app({"slug": "garten"})
    original = app.to_dict()
    monkeypatch.setattr(studio._repository, "async_save_all", AsyncMock(side_effect=OSError))
    with pytest.raises(OSError):
        await studio.async_update_app(app.app_id, {"slug": "neuer-garten"})
    with pytest.raises(OSError):
        await studio.async_delete_app(app.app_id)
    with pytest.raises(OSError):
        await studio.async_create_app({"slug": "haus"})
    assert [a.to_dict() for a in studio.list_apps()] == [original]


@pytest.mark.parametrize("launch_style", ["ripple", "glow", "aurora", "orbit", "sheen", "rise", "still"])
async def test_shell_launch_settings_and_footer(studio, launch_style):
    from custom_components.pwa_app_studio.const import VERSION
    from custom_components.pwa_app_studio.domain.models import PwaApp
    from custom_components.pwa_app_studio.presentation.http_views import PwaAppShellView

    app = await studio.async_create_app({"manifest": {"name": "Küche & Garten"}})
    legacy = app.to_dict()
    del legacy["manifest"]["launch_style"]
    del legacy["access"]["local_guests"]
    restored = PwaApp.from_dict(legacy)
    assert restored.manifest.launch_style == "ripple"
    assert not restored.access.local_guests
    app = await studio.async_update_app(app.app_id, {"manifest": {
        "name": "Küche & Garten", "launch_style": launch_style,
    }})
    assert PwaApp.from_dict(app.to_dict()).manifest.launch_style == launch_style
    shell = (await PwaAppShellView(studio).get({}, app.slug)).text
    assert f'data-style="{launch_style}"' in shell
    assert "Küche &amp; Garten" in shell
    assert f"App {VERSION} developed by seb5594 (Sebastian Schmidt)" in shell
    assert "Made with ❤️ in Germany 🇩🇪" in shell
    assert 'href="https://github.com/seb5594"' in shell
    assert "user-scalable=no" not in shell


async def test_companion_approval_requires_app_access_and_device_proof(hass, studio):
    from aiohttp import web
    from homeassistant.auth.models import TOKEN_TYPE_NORMAL
    from homeassistant.components.http.const import KEY_HASS_REFRESH_TOKEN_ID

    from custom_components.pwa_app_studio.presentation.companion_pairing import (
        CompanionApprovalView,
        CompanionPairingView,
    )

    def request(body):
        req = make_mocked_request("POST", "/", headers={
            "Host": "localhost",
            "Origin": "http://localhost",
            "Content-Type": "application/json",
            "Content-Length": "100",
        })
        req.json = AsyncMock(return_value=body)
        return req

    app = await studio.async_create_app({"slug": "pairing"})
    pending = hass.data[DOMAIN]["runtime"].pairing_requests
    device = CompanionPairingView(hass, pending)
    approval = CompanionApprovalView(hass, pending)
    with pytest.raises(web.HTTPNotFound):
        await device.post(request({}), app.slug)
    app = await studio.async_update_app(app.app_id, {"access": {
        "allow_companion_pairing": True, "allow_all_authenticated": False, "allowed_user_ids": ["allowed"],
    }})
    grant = await device.post(request({}), app.slug)
    data = json.loads(grant.text)
    code = data["code"]
    assert grant.headers["Cache-Control"] == "no-store"
    assert (await device.post(request({"code": code, "secret": data["secret"]}), app.slug)).status == 202
    with pytest.raises(web.HTTPNotFound):
        await device.post(request({"code": code, "secret": "wrong"}), app.slug)

    confirm = request({"code": code, "confirm": True})
    confirm[KEY_HASS_REFRESH_TOKEN_ID] = "signed-in"
    confirm["hass_user"] = SimpleNamespace(
        id="unlisted", is_admin=False, local_only=False, is_active=True, system_generated=False,
        refresh_tokens={"signed-in": SimpleNamespace(token_type=TOKEN_TYPE_NORMAL, credential=object())},
    )
    with pytest.raises(web.HTTPForbidden):
        await approval.post(confirm)
    confirm["hass_user"].id = "allowed"
    assert (await approval.post(confirm)).status == 200
    with pytest.raises(web.HTTPNotFound):
        await approval.post(confirm)
    with pytest.raises(web.HTTPForbidden):
        # The approving source session no longer exists at redemption.
        await device.post(request({"code": code, "secret": data["secret"]}), app.slug)
    with pytest.raises(web.HTTPNotFound):
        await device.post(request({"code": code, "secret": data["secret"]}), app.slug)
    expired = json.loads((await device.post(request({}), app.slug)).text)
    pending.pending[expired["code"]].expires_at = 0
    with pytest.raises(web.HTTPNotFound):
        await device.post(request(expired), app.slug)


async def test_share_qr_is_scalable_and_high_contrast(hass):
    from custom_components.pwa_app_studio.infrastructure.qr_generator import SegnoQrGenerator

    image = await SegnoQrGenerator(hass).async_generate_svg(
        "https://home.example/pwa_app_studio/app/my-garden/"
    )
    svg = ElementTree.fromstring(image)
    x, y, width, height = svg.attrib["viewBox"].split()
    assert (x, y) == ("0", "0")
    assert width == height
    assert "width" not in svg.attrib and "height" not in svg.attrib
    assert svg[0].attrib["fill"] == "#fff"
    assert svg[1].attrib["stroke"] == "#000"


async def test_android_maskable_icon_has_its_own_route(hass, studio):
    await studio.async_create_app({"slug": "icon-maskable-garden"})
    path = "/pwa_app_studio/app/icon-maskable-garden/icon-maskable-512.png"
    request = make_mocked_request("GET", path, app=hass.http.app)
    match = await hass.http.app.router.resolve(request)
    assert match["size"] == "512"
    view = hass.data[DOMAIN]["runtime"]
    from custom_components.pwa_app_studio.presentation.http_views import PwaIconView

    icons = PwaIconView(studio, view.icon_composer)
    response = await icons.get(request, **match)
    standard_request = make_mocked_request("GET", path.replace("icon-maskable-512", "icon-512"))
    standard = await icons.get(standard_request, **match)
    assert response.content_type == "image/png"
    assert response.body.startswith(b"\x89PNG\r\n\x1a\n")
    assert response.body != standard.body
