'''PWA App Studio custom integration entrypoint.'''

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from homeassistant.components import frontend, panel_custom
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .application.services import (
    DistributionService,
    ManifestBuilderService,
    PwaAppService,
)
from .const import (
    CONF_DEFAULT_BG_COLOR,
    CONF_DEFAULT_THEME_COLOR,
    CONF_SHOW_IN_SIDEBAR,
    CONF_SIDEBAR_ICON,
    CONF_SIDEBAR_TITLE,
    DEFAULT_BG_COLOR,
    DEFAULT_SHOW_IN_SIDEBAR,
    DEFAULT_SIDEBAR_ICON,
    DEFAULT_SIDEBAR_TITLE,
    DEFAULT_THEME_COLOR,
    DOMAIN,
    PANEL_URL_PATH,
    PANEL_WEBCOMPONENT,
    RUNNER_PANEL_URL_PATH,
    RUNNER_WEBCOMPONENT,
    STATIC_URL_PATH,
    VERSION,
)
from .infrastructure.icon_renderer import PillowIconComposer
from .infrastructure.lovelace_adapter import HaLovelaceAdapter, HaUserDirectoryAdapter
from .infrastructure.qr_generator import SegnoQrGenerator
from .infrastructure.storage_repository import HaStorageAppRepository
from .presentation.http_views import async_register_http_views
from .presentation.websocket_api import async_register_websocket_commands

PLATFORMS: list[Platform] = [Platform.BUTTON]


@dataclass(slots=True)
class PwaAppStudioRuntimeData:
    app_service: PwaAppService
    manifest_builder: ManifestBuilderService
    distribution_service: DistributionService
    icon_composer: PillowIconComposer
    lovelace_adapter: HaLovelaceAdapter
    user_directory: HaUserDirectoryAdapter


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    domain_store = hass.data.setdefault(DOMAIN, {})

    if not domain_store.get("initialized"):
        repository = HaStorageAppRepository(hass)
        lovelace_adapter = HaLovelaceAdapter(hass)
        user_directory = HaUserDirectoryAdapter(hass)
        icon_composer = PillowIconComposer(hass)
        qr_generator = SegnoQrGenerator(hass)

        app_service = PwaAppService(repository, lovelace_adapter)
        await app_service.async_initialize()

        manifest_builder = ManifestBuilderService()
        distribution_service = DistributionService(
            qr_generator=qr_generator,
            user_directory=user_directory,
            icon_composer=icon_composer,
        )

        runtime = PwaAppStudioRuntimeData(
            app_service=app_service,
            manifest_builder=manifest_builder,
            distribution_service=distribution_service,
            icon_composer=icon_composer,
            lovelace_adapter=lovelace_adapter,
            user_directory=user_directory,
        )
        domain_store["runtime"] = runtime

        frontend_dir = Path(__file__).parent / "frontend"
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    STATIC_URL_PATH,
                    str(frontend_dir),
                    cache_headers=False,
                )
            ]
        )
        add_extra_js_url(hass, f"{STATIC_URL_PATH}/pwa-app-studio-launcher.js?v={VERSION}")

        async_register_http_views(
            hass=hass,
            app_service=app_service,
            manifest_builder=manifest_builder,
            icon_composer=icon_composer,
        )
        async_register_websocket_commands(
            hass=hass,
            app_service=app_service,
            distribution_service=distribution_service,
            lovelace_adapter=lovelace_adapter,
            user_directory=user_directory,
        )
        domain_store["initialized"] = True

    await _async_register_panels(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_register_panels(hass: HomeAssistant, entry: ConfigEntry) -> None:
    opts = {**entry.data, **entry.options}
    show_in_sidebar = bool(opts.get(CONF_SHOW_IN_SIDEBAR, DEFAULT_SHOW_IN_SIDEBAR))
    sidebar_title = (
        str(opts.get(CONF_SIDEBAR_TITLE, DEFAULT_SIDEBAR_TITLE))
        if show_in_sidebar
        else None
    )
    sidebar_icon = (
        str(opts.get(CONF_SIDEBAR_ICON, DEFAULT_SIDEBAR_ICON))
        if show_in_sidebar
        else None
    )

    _remove_panel_if_exists(hass, PANEL_URL_PATH)
    _remove_panel_if_exists(hass, RUNNER_PANEL_URL_PATH)

    # Admin-only PWA Designer Panel (sidebar_title=None hides it from sidebar when disabled)
    await panel_custom.async_register_panel(
        hass=hass,
        webcomponent_name=PANEL_WEBCOMPONENT,
        frontend_url_path=PANEL_URL_PATH,
        sidebar_title=sidebar_title,
        sidebar_icon=sidebar_icon,
        module_url=f"{STATIC_URL_PATH}/pwa-app-studio-panel.js?v={VERSION}",
        embed_iframe=False,
        require_admin=True,
        handle_safe_area=True,
        config={
            "default_theme_color": opts.get(CONF_DEFAULT_THEME_COLOR, DEFAULT_THEME_COLOR),
            "default_bg_color": opts.get(CONF_DEFAULT_BG_COLOR, DEFAULT_BG_COLOR),
            "show_in_sidebar": show_in_sidebar,
        },
    )

    # Hidden non-admin PWA runner panel mounted inside HA context provider tree
    await panel_custom.async_register_panel(
        hass=hass,
        webcomponent_name=RUNNER_WEBCOMPONENT,
        frontend_url_path=RUNNER_PANEL_URL_PATH,
        sidebar_title=None,
        sidebar_icon=None,
        module_url=f"{STATIC_URL_PATH}/pwa-app-studio-runner-panel.js?v={VERSION}",
        embed_iframe=False,
        require_admin=False,
        handle_safe_area=True,
        config={},
    )


def _remove_panel_if_exists(hass: HomeAssistant, url_path: str) -> None:
    panels = hass.data.get("frontend_panels", {})
    if url_path in panels and hasattr(frontend, "async_remove_panel"):
        frontend.async_remove_panel(hass, url_path)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    _remove_panel_if_exists(hass, PANEL_URL_PATH)
    _remove_panel_if_exists(hass, RUNNER_PANEL_URL_PATH)
    return unload_ok
