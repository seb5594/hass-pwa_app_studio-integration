'''Home Assistant Store adapter implementing PwaAppRepositoryPort.'''

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from ..const import STORAGE_KEY, STORAGE_VERSION
from ..domain.models import PwaApp

_LOGGER = logging.getLogger(__name__)


class HaStorageAppRepository:
    def __init__(self, hass: HomeAssistant) -> None:
        self._store: Store[dict[str, Any]] = Store(hass, STORAGE_VERSION, STORAGE_KEY)

    async def async_load_all(self) -> list[PwaApp]:
        raw = await self._store.async_load()
        if not raw or not isinstance(raw, dict):
            return []
        apps: list[PwaApp] = []
        for item in raw.get("apps", []):
            if not isinstance(item, dict):
                continue
            try:
                apps.append(PwaApp.from_dict(item))
            except Exception as err:  # noqa: BLE001
                _LOGGER.warning("Skipping invalid stored PWA app entry: %s", err)
        return apps

    async def async_save_all(self, apps: list[PwaApp]) -> None:
        payload = {
            "apps": [app.to_dict() for app in apps],
        }
        await self._store.async_save(payload)
