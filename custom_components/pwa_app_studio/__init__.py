'''PWA Web-App Studio custom integration entrypoint.'''

from __future__ import annotations

from dataclasses import dataclass
from inspect import signature
from pathlib import Path

from homeassistant.components import frontend, http, panel_custom
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .application.services import (
    DistributionService,
    ManifestBuilderService,
    PwaAppService,
)
from .const import (
    CONF_SHOW_IN_SIDEBAR,
    CONNECT_PANEL_URL_PATH,
    CONNECT_WEBCOMPONENT,
    DEFAULT_SHOW_IN_SIDEBAR,
    DEFAULT_SIDEBAR_ICON,
    DEFAULT_SIDEBAR_TITLE,
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
from .presentation.companion_pairing import CompanionApprovalView, CompanionPairingView, PairingRequests
from .presentation.http_views import async_register_http_views
from .presentation.websocket_api import async_register_websocket_commands

PLATFORMS: list[Platform] = [Platform.BUTTON]


@dataclass
class PwaAppStudioRuntimeData:
    app_service: PwaAppService
    manifest_builder: ManifestBuilderService
    distribution_service: DistributionService
    icon_composer: PillowIconComposer
    lovelace_adapter: HaLovelaceAdapter
    user_directory: HaUserDirectoryAdapter
    pairing_requests: PairingRequests


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if entry.title == "PWA App Studio":
        hass.config_entries.async_update_entry(entry, title=DEFAULT_SIDEBAR_TITLE)
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
            pairing_requests=PairingRequests(app_service),
        )
        domain_store["runtime"] = runtime

        frontend_dir = Path(__file__).parent / "frontend"
        if hasattr(hass.http, "async_register_static_paths"):
            await hass.http.async_register_static_paths(
                [http.StaticPathConfig(STATIC_URL_PATH, str(frontend_dir), cache_headers=False)]
            )
        else:
            hass.http.register_static_path(STATIC_URL_PATH, str(frontend_dir), cache_headers=False)

        add_extra_js_url(hass, f"{STATIC_URL_PATH}/pwa-app-studio-launcher.js?v={VERSION}")

        async_register_http_views(
            hass=hass,
            app_service=app_service,
            manifest_builder=manifest_builder,
            icon_composer=icon_composer,
        )
        hass.http.register_view(CompanionPairingView(hass, runtime.pairing_requests))
        hass.http.register_view(CompanionApprovalView(hass, runtime.pairing_requests))
        async_register_websocket_commands(
            hass=hass,
            app_service=app_service,
            distribution_service=distribution_service,
            lovelace_adapter=lovelace_adapter,
            user_directory=user_directory,
        )
        domain_store["initialized"] = True

    await _async_register_panels(hass, entry)
    domain_store["runtime"].pairing_requests.active = True
    if hasattr(hass.config_entries, "async_forward_entry_setups"):
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    else:
        # Older Core loads forwarded platforms after the parent setup has returned.
        hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, Platform.BUTTON))
    entry.async_on_unload(entry.add_update_listener(_async_reload_options))
    return True


async def _async_reload_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_register_panels(hass: HomeAssistant, entry: ConfigEntry) -> None:
    opts = {**entry.data, **entry.options}
    show_in_sidebar = bool(opts.get(CONF_SHOW_IN_SIDEBAR, DEFAULT_SHOW_IN_SIDEBAR))
    sidebar_title = DEFAULT_SIDEBAR_TITLE if show_in_sidebar else None
    sidebar_icon = DEFAULT_SIDEBAR_ICON if show_in_sidebar else None

    _remove_panel_if_exists(hass, PANEL_URL_PATH)
    _remove_panel_if_exists(hass, RUNNER_PANEL_URL_PATH)
    _remove_panel_if_exists(hass, CONNECT_PANEL_URL_PATH)

    panel_options = {}
    if "handle_safe_area" in signature(panel_custom.async_register_panel).parameters:
        panel_options["handle_safe_area"] = True

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
        config={},
        **panel_options,
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
        config={},
        **panel_options,
    )
    await panel_custom.async_register_panel(
        hass=hass,
        webcomponent_name=CONNECT_WEBCOMPONENT,
        frontend_url_path=CONNECT_PANEL_URL_PATH,
        sidebar_title=None,
        sidebar_icon=None,
        module_url=f"{STATIC_URL_PATH}/pwa-app-studio-connect-panel.js",
        embed_iframe=False,
        require_admin=False,
        config={},
        **panel_options,
    )


def _remove_panel_if_exists(hass: HomeAssistant, url_path: str) -> None:
    panels = hass.data.get("frontend_panels", {})
    if url_path in panels and hasattr(frontend, "async_remove_panel"):
        frontend.async_remove_panel(hass, url_path)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    requests = hass.data[DOMAIN]["runtime"].pairing_requests
    requests.active = False
    requests.pending.clear()
    _remove_panel_if_exists(hass, PANEL_URL_PATH)
    _remove_panel_if_exists(hass, RUNNER_PANEL_URL_PATH)
    _remove_panel_if_exists(hass, CONNECT_PANEL_URL_PATH)
    return unload_ok
