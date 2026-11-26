'''HTTP Views serving isolated PWA shells, manifests, Service Workers, icons, and runtime APIs.'''

from __future__ import annotations

import html
import json
from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from ..application.ports import IconComposerPort
from ..application.services import ManifestBuilderService, PwaAppService
from ..const import API_BASE_PATH, HTTP_BASE_PATH, STATIC_URL_PATH, VERSION
from ..domain.models import PwaIconSpec


class PwaAppShellView(HomeAssistantView):
    '''Serves the public installable PWA shell HTML (no sensitive data included).'''

    url = f"{HTTP_BASE_PATH}/app/{{slug}}"
    extra_urls = [f"{HTTP_BASE_PATH}/app/{{slug}}/", f"{HTTP_BASE_PATH}/share/{{slug}}"]
    name = "pwa_app_studio:app_shell"
    requires_auth = False

    def __init__(self, app_service: PwaAppService) -> None:
        self._app_service = app_service

    async def get(self, request: web.Request, slug: str) -> web.Response:
        app = self._app_service.get_app_by_slug(slug)
        if app is None:
            return web.Response(status=404, text="PWA App not found")

        base = f"{HTTP_BASE_PATH}/app/{app.slug}"
        escaped_name = html.escape(app.manifest.name)
        escaped_theme = html.escape(app.manifest.theme_color)
        escaped_bg = html.escape(app.manifest.background_color)
        escaped_slug = html.escape(app.slug)
        ver = app.version

        body = f"""<!DOCTYPE html>
<html lang="{html.escape(app.manifest.lang)}" dir="{html.escape(app.manifest.text_dir)}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{escaped_name}</title>
  <meta name="theme-color" content="{escaped_theme}" />
  <meta name="background-color" content="{escaped_bg}" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="apple-mobile-web-app-title" content="{html.escape(app.manifest.short_name)}" />
  <link rel="icon" type="image/png" sizes="192x192" href="{base}/icon-192.png?v={ver}" />
  <link rel="apple-touch-icon" sizes="180x180" href="{base}/icon-180.png?v={ver}" />
  <link rel="manifest" href="{base}/manifest.webmanifest?v={ver}" />
  <link rel="stylesheet" href="{STATIC_URL_PATH}/pwa-shell.css" />
  <style>:root {{ --app-accent: {escaped_theme}; --app-bg: {escaped_bg}; }}</style>
</head>
<body>
  <div id="pwa-root"
       data-slug="{escaped_slug}"
       data-name="{escaped_name}"
       data-base="{base}/"
       data-sw-url="{base}/sw.js?v={ver}"
       data-client-url="{base}/client"
       data-companion-pairing="{str(app.access.allow_companion_pairing).lower()}"
       data-theme="{escaped_theme}"
       data-bg="{escaped_bg}">
    <main class="launch" data-style="{app.manifest.launch_style}">
      <div class="welcome">
        <div class="mark"><img src="{base}/icon-192.png?v={ver}" width="76" height="76" alt="" /></div>
        <h1>{escaped_name}</h1>
        <p role="status" id="launch-status">Deine App wird geöffnet …</p>
      </div>
    </main>
  </div>
  <footer><a href="https://github.com/seb5594" target="_blank" rel="noopener noreferrer">
    App {html.escape(VERSION)} developed by seb5594 (Sebastian Schmidt)<br />
    Made with ❤️ in Germany 🇩🇪</a></footer>
  <script type="module" src="{STATIC_URL_PATH}/pwa-runtime.js"></script>
</body>
</html>
"""
        return web.Response(
            text=body,
            content_type="text/html",
            charset="utf-8",
            headers={"Cache-Control": "no-cache"},
        )


class PwaManifestView(HomeAssistantView):
    url = f"{HTTP_BASE_PATH}/app/{{slug}}/manifest.webmanifest"
    name = "pwa_app_studio:manifest"
    requires_auth = False

    def __init__(
        self, app_service: PwaAppService, builder: ManifestBuilderService
    ) -> None:
        self._app_service = app_service
        self._builder = builder

    async def get(self, request: web.Request, slug: str) -> web.Response:
        app = self._app_service.get_app_by_slug(slug)
        if app is None:
            return web.Response(status=404, text="Manifest not found")
        manifest_dict = self._builder.build_manifest(app)
        return web.Response(
            text=json.dumps(manifest_dict, ensure_ascii=False, indent=2),
            content_type="application/manifest+json",
            charset="utf-8",
            headers={"Cache-Control": "no-cache"},
        )


class PwaServiceWorkerView(HomeAssistantView):
    '''Serves per-app scoped Service Worker with Service-Worker-Allowed header.'''

    url = f"{HTTP_BASE_PATH}/app/{{slug}}/sw.js"
    name = "pwa_app_studio:service_worker"
    requires_auth = False

    def __init__(self, app_service: PwaAppService) -> None:
        self._app_service = app_service

    async def get(self, request: web.Request, slug: str) -> web.Response:
        app = self._app_service.get_app_by_slug(slug)
        if app is None:
            return web.Response(status=404, text="Service worker not found")

        base = f"{HTTP_BASE_PATH}/app/{app.slug}"
        cache_name = f"pwa-app-studio:{app.slug}:{VERSION}:{app.version}"
        precache_urls = json.dumps(
            [
                f"{base}/",
                f"{base}/icon-192.png?v={app.version}",
                f"{base}/icon-512.png?v={app.version}",
                f"{base}/icon-maskable-512.png?v={app.version}",
                f"{STATIC_URL_PATH}/pwa-shell.css",
                f"{STATIC_URL_PATH}/pwa-runtime.js",
                f"{STATIC_URL_PATH}/pwa-companion-connect.js",
                f"{STATIC_URL_PATH}/pwa-install.js",
                f"{STATIC_URL_PATH}/pwa-studio-i18n.js",
            ]
        )
        offline_enabled = "true" if app.manifest.offline_enabled else "false"
        sw_js = f"""const CACHE_NAME = {json.dumps(cache_name)};
const OFFLINE_ENABLED = {offline_enabled};
const PRECACHE_ASSETS = {precache_urls};

self.addEventListener("install", (event) => {{
  self.skipWaiting();
  if (!OFFLINE_ENABLED) return;
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      Promise.allSettled(PRECACHE_ASSETS.map((url) => cache.add(url)))
    )
  );
}});

self.addEventListener("activate", (event) => {{
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => (key.startsWith("pwa-app-studio:{app.slug}:") && key !== CACHE_NAME)
            || /^pwa-app-studio-{app.slug}-v[0-9]+$/.test(key))
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
}});

self.addEventListener("fetch", (event) => {{
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (!OFFLINE_ENABLED || url.origin !== self.location.origin ||
      !PRECACHE_ASSETS.includes(url.pathname + url.search)) return;

  event.respondWith((async () => {{
    let response;
    try {{
      response = await fetch(req);
    }} catch (error) {{
      const cached = await (await caches.open(CACHE_NAME)).match(req);
      if (cached) return cached;
      throw error;
    }}
    if (response.ok && !response.redirected) {{
      const copy = response.clone();
      event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.put(req, copy)));
    }}
    return response;
  }})());
}});
"""
        return web.Response(
            text=sw_js,
            content_type="application/javascript",
            charset="utf-8",
            headers={
                "Service-Worker-Allowed": f"{base}/",
                "Cache-Control": "no-cache, no-store, must-revalidate",
            },
        )


class PwaOAuthClientView(HomeAssistantView):
    '''IndieAuth client_id endpoint declaring the exact redirect_uri for Home Assistant.'''

    url = f"{HTTP_BASE_PATH}/app/{{slug}}/client"
    name = "pwa_app_studio:oauth_client"
    requires_auth = False

    def __init__(self, app_service: PwaAppService) -> None:
        self._app_service = app_service

    async def get(self, request: web.Request, slug: str) -> web.Response:
        app = self._app_service.get_app_by_slug(slug)
        if app is None:
            return web.Response(status=404, text="Client not found")
        origin = f"{request.scheme}://{request.host}"
        redirect_uri = f"{origin}{HTTP_BASE_PATH}/app/{app.slug}/"
        doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(app.manifest.name)}</title>
  <link rel="redirect_uri" href="{html.escape(redirect_uri)}" />
</head>
<body>
  <p>{html.escape(app.manifest.name)} - Home Assistant PWA Client</p>
</body>
</html>
"""
        return web.Response(text=doc, content_type="text/html", charset="utf-8")


class PwaIconView(HomeAssistantView):
    '''Serves dynamically composited 180, 192, 512, and maskable-512 PNG icons.'''

    url = f"{HTTP_BASE_PATH}/app/{{slug}}/icon-{{size:[0-9]+}}.png"
    extra_urls = [f"{HTTP_BASE_PATH}/app/{{slug}}/icon-maskable-{{size:[0-9]+}}.png"]
    name = "pwa_app_studio:icon"
    requires_auth = False

    def __init__(
        self, app_service: PwaAppService, icon_composer: IconComposerPort
    ) -> None:
        self._app_service = app_service
        self._icon_composer = icon_composer

    async def get(self, request: web.Request, slug: str, size: str) -> web.Response:
        app = self._app_service.get_app_by_slug(slug)
        if app is None:
            return web.Response(status=404, text="Icon not found")
        if size not in ("180", "192", "512"):
            return web.Response(status=400, text="Unsupported icon size")
        maskable = request.path.rsplit("/", 1)[-1].startswith("icon-maskable-")
        png_bytes = await self._icon_composer.async_render_png(
            app.icon,
            int(size),
            maskable=maskable,
            cache_key_suffix=f"{app.app_id}:{app.version}",
        )
        return web.Response(
            body=png_bytes,
            content_type="image/png",
            headers={"Cache-Control": "public, max-age=3600"},
        )


class PwaIconPreviewApiView(HomeAssistantView):
    '''Admin-only live icon compositor preview endpoint for the Designer UI.'''

    url = f"{API_BASE_PATH}/icon_preview"
    name = "pwa_app_studio:api_icon_preview"
    requires_auth = True

    def __init__(self, icon_composer: IconComposerPort) -> None:
        self._icon_composer = icon_composer

    async def post(self, request: web.Request) -> web.Response:
        user = request["hass_user"]
        if not user.is_admin:
            return web.json_response({"error": "admin_required"}, status=403)
        try:
            payload = await request.json()
        except Exception:  # noqa: BLE001
            return web.json_response({"error": "invalid_json"}, status=400)

        spec = PwaIconSpec.from_dict(payload.get("icon", {}))
        maskable = bool(payload.get("maskable", False))
        size = int(payload.get("size", 192))
        size = max(64, min(512, size))
        png_bytes = await self._icon_composer.async_render_png(spec, size, maskable=maskable)
        return web.Response(body=png_bytes, content_type="image/png")


class PwaRuntimeApiView(HomeAssistantView):
    '''Authenticated and ACL-checked runtime payload endpoint for PWA boot.'''

    url = f"{API_BASE_PATH}/runtime/{{slug}}"
    name = "pwa_app_studio:api_runtime"
    requires_auth = True

    def __init__(self, app_service: PwaAppService) -> None:
        self._app_service = app_service

    async def get(self, request: web.Request, slug: str) -> web.Response:
        app = self._app_service.get_app_by_slug(slug)
        if app is None:
            return web.json_response({"error": "not_found"}, status=404)

        user = request["hass_user"]
        if not user.is_active or not self._app_service.can_user_access(
            app, user.id, user.is_admin, user.local_only
        ):
            return web.json_response(
                {
                    "error": "access_denied",
                    "message": "Dieser Home-Assistant-Benutzer ist für diese PWA nicht freigeschaltet.",
                    "user": {"id": user.id, "name": user.name},
                },
                status=403,
            )

        return web.json_response(
            {
                "app_id": app.app_id,
                "slug": app.slug,
                "version": app.version,
                "manifest": app.manifest.to_dict(),
                "content": app.content.to_dict(),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "is_admin": user.is_admin,
                },
            }
        )


def async_register_http_views(
    hass: HomeAssistant,
    app_service: PwaAppService,
    manifest_builder: ManifestBuilderService,
    icon_composer: IconComposerPort,
) -> None:
    hass.http.register_view(PwaAppShellView(app_service))
    hass.http.register_view(PwaManifestView(app_service, manifest_builder))
    hass.http.register_view(PwaServiceWorkerView(app_service))
    hass.http.register_view(PwaOAuthClientView(app_service))
    hass.http.register_view(PwaIconView(app_service, icon_composer))
    hass.http.register_view(PwaIconPreviewApiView(icon_composer))
    hass.http.register_view(PwaRuntimeApiView(app_service))
