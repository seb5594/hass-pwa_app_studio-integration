'''Adapter reading Home Assistant Lovelace dashboards and registered users.'''

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class HaLovelaceAdapter:
    '''Reads LovelaceData dashboards, views, sections, and cards safely.'''

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    async def async_list_dashboards(self) -> list[dict[str, Any]]:
        lovelace_data = self._hass.data.get("lovelace")
        if lovelace_data is None:
            return []

        dashboards_map = getattr(lovelace_data, "dashboards", None)
        if not isinstance(dashboards_map, dict):
            return []

        result: list[dict[str, Any]] = []
        for url_path, dashboard in dashboards_map.items():
            normalized_path = "lovelace" if url_path is None else str(url_path)
            cfg_meta = getattr(dashboard, "config", None) or {}
            title = str(
                cfg_meta.get("title")
                or ("Übersicht" if normalized_path == "lovelace" else normalized_path)
            )
            icon = str(cfg_meta.get("icon") or "mdi:view-dashboard")
            mode = str(cfg_meta.get("mode") or getattr(lovelace_data, "resource_mode", "storage"))
            views_info: list[dict[str, Any]] = []

            try:
                raw_config = await dashboard.async_load(False)
                if isinstance(raw_config, dict):
                    for idx, view in enumerate(raw_config.get("views", [])):
                        if not isinstance(view, dict):
                            continue
                        v_path = str(view.get("path") or idx)
                        v_title = str(view.get("title") or f"Ansicht {idx + 1}")
                        v_icon = str(view.get("icon") or "")
                        cards = self._extract_cards_from_view(view)
                        views_info.append(
                            {
                                "path": v_path,
                                "title": v_title,
                                "icon": v_icon,
                                "cards": cards,
                            }
                        )
            except Exception as err:  # noqa: BLE001
                _LOGGER.debug(
                    "Could not inspect Lovelace dashboard '%s': %s", normalized_path, err
                )

            result.append(
                {
                    "url_path": normalized_path,
                    "title": title,
                    "icon": icon,
                    "mode": mode,
                    "require_admin": bool(cfg_meta.get("require_admin", False)),
                    "views": views_info,
                }
            )
        return result

    async def async_get_dashboard_icon(self, url_path: str) -> str | None:
        lovelace_data = self._hass.data.get("lovelace")
        if lovelace_data is None:
            return None
        dashboards_map = getattr(lovelace_data, "dashboards", None)
        if not isinstance(dashboards_map, dict):
            return None
        lookup_key = None if url_path in ("", "lovelace") else url_path
        dashboard = dashboards_map.get(lookup_key)
        if dashboard is None and lookup_key is not None:
            dashboard = dashboards_map.get("lovelace")
        if dashboard is None:
            return None
        cfg_meta = getattr(dashboard, "config", None) or {}
        icon = cfg_meta.get("icon")
        return str(icon) if icon else "mdi:view-dashboard"

    @staticmethod
    def _extract_cards_from_view(view: dict[str, Any]) -> list[dict[str, Any]]:
        collected: list[dict[str, Any]] = []
        for card in view.get("cards", []):
            if isinstance(card, dict):
                collected.append(card)
        for section in view.get("sections", []):
            if isinstance(section, dict):
                for card in section.get("cards", []):
                    if isinstance(card, dict):
                        collected.append(card)
        return collected


class HaUserDirectoryAdapter:
    '''Lists active human Home Assistant user accounts for ACL and QR sharing.'''

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    async def async_list_registered_users(self) -> list[dict[str, Any]]:
        users = await self._hass.auth.async_get_users()
        result: list[dict[str, Any]] = []
        for user in users:
            if user.system_generated or not user.is_active:
                continue
            result.append(
                {
                    "id": user.id,
                    "name": user.name or "Unbenannter Benutzer",
                    "is_admin": bool(user.is_admin),
                    "is_owner": bool(user.is_owner),
                }
            )
        return result
