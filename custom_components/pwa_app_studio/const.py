'''Constants for the PWA App Studio integration.'''

from __future__ import annotations

DOMAIN = "pwa_app_studio"
NAME = "PWA App Studio"
VERSION = "1.0.0"

PANEL_URL_PATH = "pwa-app-studio"
PANEL_WEBCOMPONENT = "pwa-app-studio-panel"
RUNNER_PANEL_URL_PATH = "pwa-app-studio-runner"
RUNNER_WEBCOMPONENT = "pwa-app-studio-runner-panel"

STATIC_URL_PATH = "/pwa_app_studio_static"
HTTP_BASE_PATH = "/pwa_app_studio"
API_BASE_PATH = "/api/pwa_app_studio"

EVENT_OPEN_DESIGNER = "pwa_app_studio_open_designer"

STORAGE_KEY = "pwa_app_studio.apps"
STORAGE_VERSION = 1

CONF_SHOW_IN_SIDEBAR = "show_in_sidebar"
CONF_SIDEBAR_TITLE = "sidebar_title"
CONF_SIDEBAR_ICON = "sidebar_icon"
CONF_DEFAULT_THEME_COLOR = "default_theme_color"
CONF_DEFAULT_BG_COLOR = "default_bg_color"

DEFAULT_SHOW_IN_SIDEBAR = True
DEFAULT_SIDEBAR_TITLE = "PWA App Studio"
DEFAULT_SIDEBAR_ICON = "mdi:cellphone-cog"
DEFAULT_THEME_COLOR = "#03a9f4"
DEFAULT_BG_COLOR = "#111827"
