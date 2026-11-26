'''Constants for the PWA Web-App Studio integration.'''

from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "pwa_app_studio"
NAME = "PWA Web-App Studio"
VERSION = json.loads(Path(__file__).with_name("manifest.json").read_text(encoding="utf-8"))["version"]

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

DEFAULT_SHOW_IN_SIDEBAR = True
DEFAULT_SIDEBAR_TITLE = "PWA Web-App Studio"
DEFAULT_SIDEBAR_ICON = "mdi:cellphone-cog"
