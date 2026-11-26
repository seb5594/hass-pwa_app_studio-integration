'''Abstract infrastructure ports for the application layer.'''

from __future__ import annotations

from typing import Any, Protocol

from ..domain.models import PwaApp, PwaIconSpec


class PwaAppRepositoryPort(Protocol):
    async def async_load_all(self) -> list[PwaApp]: ...

    async def async_save_all(self, apps: list[PwaApp]) -> None: ...


class LovelaceReaderPort(Protocol):
    async def async_list_dashboards(self) -> list[dict[str, Any]]: ...

    async def async_get_dashboard_icon(self, url_path: str) -> str | None: ...


class UserDirectoryPort(Protocol):
    async def async_list_registered_users(self) -> list[dict[str, Any]]: ...


class IconComposerPort(Protocol):
    async def async_render_png(
        self,
        spec: PwaIconSpec,
        size: int,
        maskable: bool = False,
        cache_key_suffix: str = "",
    ) -> bytes: ...


class QrGeneratorPort(Protocol):
    async def async_generate_svg(self, url: str) -> str: ...
