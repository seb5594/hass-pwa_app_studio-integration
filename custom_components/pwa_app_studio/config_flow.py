'''ConfigFlow and OptionsFlowWithReload for PWA App Studio.'''

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.core import callback

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
)


def _build_schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_SHOW_IN_SIDEBAR,
                default=defaults.get(CONF_SHOW_IN_SIDEBAR, DEFAULT_SHOW_IN_SIDEBAR),
            ): bool,
            vol.Required(
                CONF_SIDEBAR_TITLE,
                default=defaults.get(CONF_SIDEBAR_TITLE, DEFAULT_SIDEBAR_TITLE),
            ): str,
            vol.Required(
                CONF_SIDEBAR_ICON,
                default=defaults.get(CONF_SIDEBAR_ICON, DEFAULT_SIDEBAR_ICON),
            ): str,
            vol.Required(
                CONF_DEFAULT_THEME_COLOR,
                default=defaults.get(CONF_DEFAULT_THEME_COLOR, DEFAULT_THEME_COLOR),
            ): str,
            vol.Required(
                CONF_DEFAULT_BG_COLOR,
                default=defaults.get(CONF_DEFAULT_BG_COLOR, DEFAULT_BG_COLOR),
            ): str,
        }
    )


class PwaAppStudioConfigFlow(ConfigFlow, domain=DOMAIN):
    '''Handle a config flow for PWA App Studio.'''

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="PWA App Studio",
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
        return PwaAppStudioOptionsFlow()


class PwaAppStudioOptionsFlow(OptionsFlowWithReload):
    '''Options flow that automatically reloads the integration on save.'''

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(current),
        )
