'''Configuration and sidebar options for PWA Web-App Studio.'''

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
)
from homeassistant.core import callback

from .const import (
    CONF_SHOW_IN_SIDEBAR,
    DEFAULT_SHOW_IN_SIDEBAR,
    DOMAIN,
)


def _build_schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_SHOW_IN_SIDEBAR,
                default=defaults.get(CONF_SHOW_IN_SIDEBAR, DEFAULT_SHOW_IN_SIDEBAR),
            ): bool,
        }
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
                options=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema({}),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> PwaAppStudioOptionsFlow:
        return PwaAppStudioOptionsFlow(config_entry)


class PwaAppStudioOptionsFlow(OptionsFlow):
    """Store the sidebar option. The config entry listener applies it."""

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self._entry.data, **self._entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(current),
        )
