'''Application use-case services for PWA Web-App Studio.'''

from __future__ import annotations

import asyncio
from typing import Any

from ..const import HTTP_BASE_PATH
from ..domain.models import (
    IconMode,
    PwaAccessPolicy,
    PwaApp,
    PwaContentSpec,
    PwaIconSpec,
    PwaManifestOptions,
    utc_now_iso,
    validate_slug,
)
from .ports import (
    IconComposerPort,
    LovelaceReaderPort,
    PwaAppRepositoryPort,
    QrGeneratorPort,
    UserDirectoryPort,
)


class PwaAppService:
    '''Manages CRUD lifecycle and authorization checks for unlimited PWA apps.'''

    def __init__(
        self,
        repository: PwaAppRepositoryPort,
        lovelace_reader: LovelaceReaderPort,
    ) -> None:
        self._repository = repository
        self._lovelace_reader = lovelace_reader
        self._apps: dict[str, PwaApp] = {}
        self._lock = asyncio.Lock()

    async def async_initialize(self) -> None:
        async with self._lock:
            loaded = await self._repository.async_load_all()
            self._apps = {app.app_id: app for app in loaded}

    def list_apps(self) -> list[PwaApp]:
        return sorted(self._apps.values(), key=lambda a: a.created_at)

    def get_app(self, app_id: str) -> PwaApp | None:
        return self._apps.get(app_id)

    def get_app_by_slug(self, slug: str) -> PwaApp | None:
        normalized = slug.strip().lower()
        for app in self._apps.values():
            if app.slug == normalized:
                return app
        return None

    async def async_create_app(self, payload: dict[str, Any]) -> PwaApp:
        async with self._lock:
            app = PwaApp.create_new(payload)
            app.slug = self._ensure_unique_slug(app.slug)
            await self._resolve_dashboard_icon(app)
            self._apps[app.app_id] = app
            await self._repository.async_save_all(self.list_apps())
            return app

    async def async_update_app(self, app_id: str, payload: dict[str, Any]) -> PwaApp:
        async with self._lock:
            existing = self._apps.get(app_id)
            if existing is None:
                raise KeyError(f"Unknown PWA app_id: {app_id}")

            if "slug" in payload and payload["slug"]:
                candidate = validate_slug(str(payload["slug"]))
                if candidate != existing.slug:
                    for other in self._apps.values():
                        if other.app_id != app_id and other.slug == candidate:
                            raise ValueError(f"Slug '{candidate}' is already in use.")
                    existing.slug = candidate

            if "manifest" in payload:
                existing.manifest = PwaManifestOptions.from_dict(payload["manifest"])
            if "content" in payload:
                existing.content = PwaContentSpec.from_dict(payload["content"])
            if "icon" in payload:
                existing.icon = PwaIconSpec.from_dict(payload["icon"])
            if "access" in payload:
                existing.access = PwaAccessPolicy.from_dict(payload["access"])

            await self._resolve_dashboard_icon(existing)
            existing.updated_at = utc_now_iso()
            existing.version += 1
            await self._repository.async_save_all(self.list_apps())
            return existing

    async def async_delete_app(self, app_id: str) -> bool:
        async with self._lock:
            if app_id not in self._apps:
                return False
            del self._apps[app_id]
            await self._repository.async_save_all(self.list_apps())
            return True

    def can_user_access(self, app: PwaApp, user_id: str, is_admin: bool) -> bool:
        return app.access.is_user_allowed(user_id=user_id, is_admin=is_admin)

    def _ensure_unique_slug(self, base_slug: str) -> str:
        used = {app.slug for app in self._apps.values()}
        if base_slug not in used:
            return base_slug
        idx = 2
        while True:
            candidate = f"{base_slug[:44]}-{idx}"
            if candidate not in used:
                return candidate
            idx += 1

    async def _resolve_dashboard_icon(self, app: PwaApp) -> None:
        if app.icon.mode == IconMode.DASHBOARD_DEFAULT:
            dash_icon = await self._lovelace_reader.async_get_dashboard_icon(
                app.content.dashboard_url_path
            )
            app.icon.resolved_dashboard_icon = dash_icon or "mdi:view-dashboard"


class ManifestBuilderService:
    '''Produces strictly typed W3C Web App Manifest dictionaries.'''

    def build_manifest(self, app: PwaApp) -> dict[str, Any]:
        app_base = f"{HTTP_BASE_PATH}/app/{app.slug}"
        start_url = f"{app_base}/"
        ver = app.version

        icons = [
            {
                "src": f"{app_base}/icon-192.png?v={ver}",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": f"{app_base}/icon-512.png?v={ver}",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": f"{app_base}/icon-maskable-512.png?v={ver}",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable",
            },
        ]

        shortcuts: list[dict[str, Any]] = []
        for shortcut in app.manifest.shortcuts[:4]:
            suffix = shortcut.url_suffix.lstrip("/")
            sc_url = f"{start_url}?target={suffix}" if suffix else start_url
            shortcuts.append(
                {
                    "name": shortcut.name,
                    "short_name": shortcut.short_name,
                    "description": shortcut.description,
                    "url": sc_url,
                    "icons": [
                        {
                            "src": f"{app_base}/icon-192.png?v={ver}",
                            "sizes": "192x192",
                            "type": "image/png",
                        }
                    ],
                }
            )

        manifest: dict[str, Any] = {
            "id": start_url,
            "name": app.manifest.name,
            "short_name": app.manifest.short_name,
            "description": app.manifest.description,
            "start_url": start_url,
            "scope": start_url,
            "display": app.manifest.display.value,
            "orientation": app.manifest.orientation.value,
            "theme_color": app.manifest.theme_color,
            "background_color": app.manifest.background_color,
            "lang": app.manifest.lang,
            "dir": app.manifest.text_dir,
            "categories": app.manifest.categories,
            "prefer_related_applications": bool(app.manifest.prefer_related_applications),
            "icons": icons,
        }
        if shortcuts:
            manifest["shortcuts"] = shortcuts
        return manifest


class DistributionService:
    '''Computes share URLs, IndieAuth parameters, and QR payloads.'''

    def __init__(
        self,
        qr_generator: QrGeneratorPort,
        user_directory: UserDirectoryPort,
        icon_composer: IconComposerPort,
    ) -> None:
        self._qr_generator = qr_generator
        self._user_directory = user_directory
        self._icon_composer = icon_composer

    async def async_build_distribution_info(
        self,
        app: PwaApp,
        base_url: str,
    ) -> dict[str, Any]:
        clean_base = base_url.rstrip("/")
        app_path = f"{HTTP_BASE_PATH}/app/{app.slug}/"
        launch_url = f"{clean_base}{app_path}" if clean_base else app_path
        qr_svg = await self._qr_generator.async_generate_svg(launch_url)
        all_users = await self._user_directory.async_list_registered_users()
        permitted = [
            user
            for user in all_users
            if app.access.is_user_allowed(user["id"], user["is_admin"])
        ]
        return {
            "app_id": app.app_id,
            "slug": app.slug,
            "launch_url": launch_url,
            "manifest_url": f"{launch_url}manifest.webmanifest?v={app.version}",
            "client_id": f"{launch_url}client",
            "qr_svg": qr_svg,
            "permitted_users": permitted,
        }
