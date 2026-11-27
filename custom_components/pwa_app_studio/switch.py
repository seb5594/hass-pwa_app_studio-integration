"""Sidebar visibility control for PWA Web-App Studio."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_SHOW_IN_SIDEBAR, DEFAULT_SHOW_IN_SIDEBAR, DOMAIN, NAME


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([SidebarPanelSwitch(entry)])


class SidebarPanelSwitch(SwitchEntity):
    """Show or hide the administrator shortcut in the sidebar."""

    _attr_has_entity_name = True
    _attr_translation_key = "sidebar_panel"
    _attr_icon = "mdi:dock-left"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_enabled_default = False
    _attr_should_poll = False

    if not hasattr(SwitchEntity, "translation_key"):
        _attr_name = "Sidebar Panel"

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_sidebar_panel"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}, "name": NAME}

    @property
    def is_on(self) -> bool:
        options = {**self._entry.data, **self._entry.options}
        return bool(options.get(CONF_SHOW_IN_SIDEBAR, DEFAULT_SHOW_IN_SIDEBAR))

    async def async_turn_on(self, **kwargs) -> None:
        await self._set_sidebar(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._set_sidebar(False)

    async def _set_sidebar(self, value: bool) -> None:
        user_id = self._context.user_id if self._context else None
        if user_id:
            user = await self.hass.auth.async_get_user(user_id)
            if not user or not user.is_admin:
                raise HomeAssistantError("Only administrators can change the Studio sidebar.")
        self.hass.config_entries.async_update_entry(
            self._entry, options={**self._entry.options, CONF_SHOW_IN_SIDEBAR: value},
        )
        self.async_write_ha_state()
