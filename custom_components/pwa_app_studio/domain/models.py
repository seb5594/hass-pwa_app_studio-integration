'''Pure domain entities, value objects, and validation rules for PWA App Studio.'''

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
import re
from typing import Any
import uuid

SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{1,48}$")
HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


class ContentSourceMode(StrEnum):
    LOVELACE_DASHBOARD = "lovelace_dashboard"
    LOVELACE_CARDS = "lovelace_cards"


class CardLayoutMode(StrEnum):
    STACK = "stack"
    GRID = "grid"
    MASONRY = "masonry"


class IconMode(StrEnum):
    HA_DEFAULT = "ha_default"
    MDI_ICON = "mdi_icon"
    HA_WITH_BADGE = "ha_with_badge"
    ICON_WITH_HA_BADGE = "icon_with_ha_badge"
    UPLOADED = "uploaded"
    DASHBOARD_DEFAULT = "dashboard_default"


class BadgePosition(StrEnum):
    BOTTOM_RIGHT = "bottom_right"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    TOP_LEFT = "top_left"


class DisplayMode(StrEnum):
    STANDALONE = "standalone"
    FULLSCREEN = "fullscreen"
    MINIMAL_UI = "minimal-ui"
    BROWSER = "browser"


class OrientationMode(StrEnum):
    ANY = "any"
    NATURAL = "natural"
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class DevicePreviewTarget(StrEnum):
    DESKTOP = "desktop"
    TABLET = "tablet"
    SMARTPHONE = "smartphone"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_hex_color(value: str | None, fallback: str) -> str:
    if not value or not isinstance(value, str):
        return fallback
    cleaned = value.strip()
    if HEX_COLOR_PATTERN.match(cleaned):
        return cleaned.lower()
    return fallback


def slugify_name(raw_value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9_-]+", "-", raw_value.strip().lower()).strip("-_")
    if len(cleaned) < 2:
        cleaned = f"app-{uuid.uuid4().hex[:6]}"
    return cleaned[:48]


def validate_slug(raw_slug: str) -> str:
    candidate = raw_slug.strip().lower()
    if not SLUG_PATTERN.match(candidate):
        raise ValueError(
            "Slug must be 2-49 characters containing lowercase letters, numbers, '-' or '_'."
        )
    return candidate


@dataclass(slots=True)
class PwaCardItem:
    id: str
    order: int
    title: str = ""
    col_span: int = 1
    config: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any], default_order: int = 0) -> PwaCardItem:
        cfg = data.get("config")
        if not isinstance(cfg, dict):
            cfg = {"type": "markdown", "content": "Leere Karte"}
        span = int(data.get("col_span", 1))
        span = max(1, min(4, span))
        return cls(
            id=str(data.get("id") or uuid.uuid4().hex[:10]),
            order=int(data.get("order", default_order)),
            title=str(data.get("title") or ""),
            col_span=span,
            config=dict(cfg),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order": self.order,
            "title": self.title,
            "col_span": self.col_span,
            "config": self.config,
        }


@dataclass(slots=True)
class PwaShortcut:
    name: str
    short_name: str
    url_suffix: str
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PwaShortcut:
        name = str(data.get("name") or "Ansicht").strip()[:48]
        short_name = str(data.get("short_name") or name).strip()[:24]
        suffix = str(data.get("url_suffix") or "").strip()
        return cls(
            name=name,
            short_name=short_name,
            url_suffix=suffix,
            description=str(data.get("description") or "")[:120],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "short_name": self.short_name,
            "url_suffix": self.url_suffix,
            "description": self.description,
        }


@dataclass(slots=True)
class PwaIconSpec:
    mode: IconMode = IconMode.HA_DEFAULT
    mdi_icon: str = "mdi:home-assistant"
    icon_svg_path: str = ""
    icon_color: str = "#ffffff"
    bg_color: str = "#03a9f4"
    badge_icon: str = "mdi:lightbulb"
    badge_svg_path: str = ""
    badge_color: str = "#ffffff"
    badge_bg_color: str = "#111827"
    badge_position: BadgePosition = BadgePosition.BOTTOM_RIGHT
    uploaded_image_b64: str = ""
    uploaded_mime: str = "image/png"
    corner_radius_pct: int = 22
    maskable_padding_pct: int = 12
    resolved_dashboard_icon: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PwaIconSpec:
        mode_raw = str(data.get("mode", IconMode.HA_DEFAULT.value))
        try:
            mode = IconMode(mode_raw)
        except ValueError:
            mode = IconMode.HA_DEFAULT

        pos_raw = str(data.get("badge_position", BadgePosition.BOTTOM_RIGHT.value))
        try:
            pos = BadgePosition(pos_raw)
        except ValueError:
            pos = BadgePosition.BOTTOM_RIGHT

        radius = max(0, min(50, int(data.get("corner_radius_pct", 22))))
        padding = max(0, min(30, int(data.get("maskable_padding_pct", 12))))

        return cls(
            mode=mode,
            mdi_icon=str(data.get("mdi_icon") or "mdi:home-assistant").strip(),
            icon_svg_path=str(data.get("icon_svg_path") or "").strip(),
            icon_color=normalize_hex_color(data.get("icon_color"), "#ffffff"),
            bg_color=normalize_hex_color(data.get("bg_color"), "#03a9f4"),
            badge_icon=str(data.get("badge_icon") or "mdi:lightbulb").strip(),
            badge_svg_path=str(data.get("badge_svg_path") or "").strip(),
            badge_color=normalize_hex_color(data.get("badge_color"), "#ffffff"),
            badge_bg_color=normalize_hex_color(data.get("badge_bg_color"), "#111827"),
            badge_position=pos,
            uploaded_image_b64=str(data.get("uploaded_image_b64") or ""),
            uploaded_mime=str(data.get("uploaded_mime") or "image/png"),
            corner_radius_pct=radius,
            maskable_padding_pct=padding,
            resolved_dashboard_icon=str(data.get("resolved_dashboard_icon") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode.value,
            "mdi_icon": self.mdi_icon,
            "icon_svg_path": self.icon_svg_path,
            "icon_color": self.icon_color,
            "bg_color": self.bg_color,
            "badge_icon": self.badge_icon,
            "badge_svg_path": self.badge_svg_path,
            "badge_color": self.badge_color,
            "badge_bg_color": self.badge_bg_color,
            "badge_position": self.badge_position.value,
            "uploaded_image_b64": self.uploaded_image_b64,
            "uploaded_mime": self.uploaded_mime,
            "corner_radius_pct": self.corner_radius_pct,
            "maskable_padding_pct": self.maskable_padding_pct,
            "resolved_dashboard_icon": self.resolved_dashboard_icon,
        }


@dataclass(slots=True)
class PwaManifestOptions:
    name: str = "Home Assistant App"
    short_name: str = "HA App"
    description: str = "Home Assistant Progressive Web App"
    display: DisplayMode = DisplayMode.STANDALONE
    orientation: OrientationMode = OrientationMode.ANY
    theme_color: str = "#03a9f4"
    background_color: str = "#111827"
    lang: str = "de"
    text_dir: str = "ltr"
    categories: list[str] = field(default_factory=lambda: ["utilities", "lifestyle"])
    shortcuts: list[PwaShortcut] = field(default_factory=list)
    prefer_related_applications: bool = False
    offline_enabled: bool = True
    cache_strategy: str = "network_first"
    hide_ha_header: bool = True
    hide_ha_sidebar: bool = True
    kiosk_mode: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PwaManifestOptions:
        try:
            display = DisplayMode(str(data.get("display", DisplayMode.STANDALONE.value)))
        except ValueError:
            display = DisplayMode.STANDALONE
        try:
            orientation = OrientationMode(
                str(data.get("orientation", OrientationMode.ANY.value))
            )
        except ValueError:
            orientation = OrientationMode.ANY

        shortcuts = [
            PwaShortcut.from_dict(item)
            for item in data.get("shortcuts", [])
            if isinstance(item, dict)
        ]
        cats = [str(c).strip() for c in data.get("categories", []) if str(c).strip()]
        if not cats:
            cats = ["utilities"]

        name = str(data.get("name") or "Home Assistant App").strip()[:64]
        short_name = str(data.get("short_name") or name).strip()[:20]
        text_dir = str(data.get("dir", data.get("text_dir", "ltr"))).lower()
        if text_dir not in ("ltr", "rtl", "auto"):
            text_dir = "ltr"

        return cls(
            name=name,
            short_name=short_name,
            description=str(data.get("description") or "").strip()[:240],
            display=display,
            orientation=orientation,
            theme_color=normalize_hex_color(data.get("theme_color"), "#03a9f4"),
            background_color=normalize_hex_color(data.get("background_color"), "#111827"),
            lang=str(data.get("lang") or "de").strip()[:12],
            text_dir=text_dir,
            categories=cats,
            shortcuts=shortcuts,
            prefer_related_applications=bool(data.get("prefer_related_applications", False)),
            offline_enabled=bool(data.get("offline_enabled", True)),
            cache_strategy=str(data.get("cache_strategy") or "network_first"),
            hide_ha_header=bool(data.get("hide_ha_header", True)),
            hide_ha_sidebar=bool(data.get("hide_ha_sidebar", True)),
            kiosk_mode=bool(data.get("kiosk_mode", False)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "short_name": self.short_name,
            "description": self.description,
            "display": self.display.value,
            "orientation": self.orientation.value,
            "theme_color": self.theme_color,
            "background_color": self.background_color,
            "lang": self.lang,
            "dir": self.text_dir,
            "categories": self.categories,
            "shortcuts": [s.to_dict() for s in self.shortcuts],
            "prefer_related_applications": self.prefer_related_applications,
            "offline_enabled": self.offline_enabled,
            "cache_strategy": self.cache_strategy,
            "hide_ha_header": self.hide_ha_header,
            "hide_ha_sidebar": self.hide_ha_sidebar,
            "kiosk_mode": self.kiosk_mode,
        }


@dataclass(slots=True)
class PwaContentSpec:
    source_mode: ContentSourceMode = ContentSourceMode.LOVELACE_DASHBOARD
    dashboard_url_path: str = "lovelace"
    view_path: str = ""
    cards: list[PwaCardItem] = field(default_factory=list)
    layout_mode: CardLayoutMode = CardLayoutMode.GRID
    grid_columns: int = 2
    default_preview_device: DevicePreviewTarget = DevicePreviewTarget.SMARTPHONE

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PwaContentSpec:
        try:
            source_mode = ContentSourceMode(
                str(data.get("source_mode", ContentSourceMode.LOVELACE_DASHBOARD.value))
            )
        except ValueError:
            source_mode = ContentSourceMode.LOVELACE_DASHBOARD

        try:
            layout_mode = CardLayoutMode(
                str(data.get("layout_mode", CardLayoutMode.GRID.value))
            )
        except ValueError:
            layout_mode = CardLayoutMode.GRID

        try:
            preview = DevicePreviewTarget(
                str(data.get("default_preview_device", DevicePreviewTarget.SMARTPHONE.value))
            )
        except ValueError:
            preview = DevicePreviewTarget.SMARTPHONE

        raw_cards = data.get("cards", [])
        cards = [
            PwaCardItem.from_dict(item, default_order=idx)
            for idx, item in enumerate(raw_cards)
            if isinstance(item, dict)
        ]
        cards.sort(key=lambda c: c.order)
        for idx, card in enumerate(cards):
            card.order = idx

        grid_cols = max(1, min(4, int(data.get("grid_columns", 2))))

        return cls(
            source_mode=source_mode,
            dashboard_url_path=str(data.get("dashboard_url_path") or "lovelace").strip(),
            view_path=str(data.get("view_path") or "").strip(),
            cards=cards,
            layout_mode=layout_mode,
            grid_columns=grid_cols,
            default_preview_device=preview,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_mode": self.source_mode.value,
            "dashboard_url_path": self.dashboard_url_path,
            "view_path": self.view_path,
            "cards": [c.to_dict() for c in sorted(self.cards, key=lambda x: x.order)],
            "layout_mode": self.layout_mode.value,
            "grid_columns": self.grid_columns,
            "default_preview_device": self.default_preview_device.value,
        }


@dataclass(slots=True)
class PwaAccessPolicy:
    allow_all_authenticated: bool = True
    allowed_user_ids: list[str] = field(default_factory=list)
    require_admin: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PwaAccessPolicy:
        users = [str(u).strip() for u in data.get("allowed_user_ids", []) if str(u).strip()]
        return cls(
            allow_all_authenticated=bool(data.get("allow_all_authenticated", True)),
            allowed_user_ids=list(dict.fromkeys(users)),
            require_admin=bool(data.get("require_admin", False)),
        )

    def is_user_allowed(self, user_id: str, is_admin: bool) -> bool:
        if is_admin:
            return True
        if self.require_admin:
            return False
        if self.allow_all_authenticated:
            return True
        return user_id in self.allowed_user_ids

    def to_dict(self) -> dict[str, Any]:
        return {
            "allow_all_authenticated": self.allow_all_authenticated,
            "allowed_user_ids": self.allowed_user_ids,
            "require_admin": self.require_admin,
        }


@dataclass(slots=True)
class PwaApp:
    app_id: str
    slug: str
    created_at: str
    updated_at: str
    version: int
    manifest: PwaManifestOptions
    content: PwaContentSpec
    icon: PwaIconSpec
    access: PwaAccessPolicy

    @classmethod
    def create_new(cls, payload: dict[str, Any]) -> PwaApp:
        manifest = PwaManifestOptions.from_dict(payload.get("manifest", {}))
        raw_slug = str(payload.get("slug") or "").strip()
        slug = validate_slug(raw_slug) if raw_slug else slugify_name(manifest.name)
        now = utc_now_iso()
        return cls(
            app_id=str(payload.get("app_id") or uuid.uuid4().hex[:12]),
            slug=slug,
            created_at=now,
            updated_at=now,
            version=1,
            manifest=manifest,
            content=PwaContentSpec.from_dict(payload.get("content", {})),
            icon=PwaIconSpec.from_dict(payload.get("icon", {})),
            access=PwaAccessPolicy.from_dict(payload.get("access", {})),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PwaApp:
        return cls(
            app_id=str(data["app_id"]),
            slug=validate_slug(str(data["slug"])),
            created_at=str(data.get("created_at") or utc_now_iso()),
            updated_at=str(data.get("updated_at") or utc_now_iso()),
            version=max(1, int(data.get("version", 1))),
            manifest=PwaManifestOptions.from_dict(data.get("manifest", {})),
            content=PwaContentSpec.from_dict(data.get("content", {})),
            icon=PwaIconSpec.from_dict(data.get("icon", {})),
            access=PwaAccessPolicy.from_dict(data.get("access", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "app_id": self.app_id,
            "slug": self.slug,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "manifest": self.manifest.to_dict(),
            "content": self.content.to_dict(),
            "icon": self.icon.to_dict(),
            "access": self.access.to_dict(),
        }
