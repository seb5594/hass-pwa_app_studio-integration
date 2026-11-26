"""The integration inside a genuine Home Assistant core.

They need Home Assistant and pytest-homeassistant-custom-component. The shared
engine installs both for every release the Compatibility workflow lists; to run them
locally: python .engine/.scripts/ha_matrix.py run 2026.9.4
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

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


async def test_shell_launch_settings_and_footer(studio):
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
        "name": "Küche & Garten", "launch_style": "still",
    }})
    shell = (await PwaAppShellView(studio).get({}, app.slug)).text
    assert 'data-style="still"' in shell
    assert "Küche &amp; Garten" in shell
    assert f"App {VERSION} developed by seb5594 (Sebastian Schmidt)" in shell
    assert "Made with ❤️ in Germany 🇩🇪" in shell
    assert 'href="https://github.com/seb5594"' in shell
    assert "user-scalable=no" not in shell
