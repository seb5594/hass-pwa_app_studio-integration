'''Configuration and sidebar options for PWA Web-App Studio.'''

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
)
from homeassistant.core import callback

from .const import (
    DOMAIN,
    PANEL_URL_PATH,
)


class PwaAppStudioConfigFlow(ConfigFlow, domain=DOMAIN):
    '''Handle a config flow for PWA Web-App Studio.'''

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="PWA Web-App Studio",
                data={},
            )

        return self.async_show_form(
            step_id="user",
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> PwaAppStudioOptionsFlow:
        return PwaAppStudioOptionsFlow(config_entry)


class PwaAppStudioOptionsFlow(OptionsFlow):
    """Open the admin Studio panel through Home Assistant's options dialog."""

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if user_input is not None:
            return self.async_external_step_done(next_step_id="finish")
        return self.async_external_step(
            step_id="init", url=f"/{PANEL_URL_PATH}?studio_options={self.flow_id}",
        )

    async def async_step_finish(self, user_input: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.async_create_entry(title="", data=dict(self._entry.options))
