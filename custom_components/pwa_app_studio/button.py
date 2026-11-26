'''Button entity dynamically opening the admin-only PWA Designer.'''

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, EVENT_OPEN_DESIGNER, NAME, PANEL_URL_PATH, VERSION


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([PwaAppStudioOpenDesignerButton(entry)])


class PwaAppStudioOpenDesignerButton(ButtonEntity):
    '''Admin-guarded button entity that launches the PWA Designer panel.'''

    _attr_has_entity_name = True
    _attr_translation_key = "open_designer"
    _attr_icon = "mdi:cellphone-cog"
    _attr_entity_category = EntityCategory.CONFIG

    if not hasattr(ButtonEntity, "translation_key"):
        _attr_name = "Open PWA Web-App Studio"

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_open_designer"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": NAME,
            "manufacturer": "PWA Web-App Studio",
            "configuration_url": f"homeassistant://navigate/{PANEL_URL_PATH}",
            "model": "Home Assistant PWA Builder",
            "sw_version": VERSION,
        }

    async def async_press(self) -> None:
        triggered_by = self._context.user_id if self._context else None
        if triggered_by is not None:
            user = await self.hass.auth.async_get_user(triggered_by)
            if user is None or not user.is_admin:
                raise HomeAssistantError(
                    "Nur Administratoren dürfen den PWA Designer öffnen."
                )

        self.hass.bus.async_fire(
            EVENT_OPEN_DESIGNER,
            {
                "panel_path": f"/{PANEL_URL_PATH}",
                "triggered_by": triggered_by,
            },
        )
