'''Pure Pillow + SVG path compositor for all 6 PWA icon modes.'''

from __future__ import annotations

import base64
from collections import OrderedDict
import hashlib
import io
import json
import logging
import math
from pathlib import Path
import re

from PIL import Image, ImageDraw
from homeassistant.core import HomeAssistant

from ..domain.models import BadgePosition, IconMode, PwaIconSpec

_LOGGER = logging.getLogger(__name__)
_LANCZOS = getattr(Image, "Resampling", Image).LANCZOS

# Built-in fallback SVG 24x24 paths for common dashboard / MDI icons
BUILTIN_MDI_PATHS: dict[str, str] = {
    "mdi:home": "M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z",
    "mdi:home-assistant": "M12,2L2,12H5V20H19V12H22L12,2M12,7.5A1.5,1.5 0 0,1 13.5,9A1.5,1.5 0 0,1 12,10.5A1.5,1.5 0 0,1 10.5,9A1.5,1.5 0 0,1 12,7.5M12,11.5A1.5,1.5 0 0,1 13.5,13A1.5,1.5 0 0,1 12,14.5A1.5,1.5 0 0,1 10.5,13A1.5,1.5 0 0,1 12,11.5M9,14.5A1.5,1.5 0 0,1 10.5,16A1.5,1.5 0 0,1 9,17.5A1.5,1.5 0 0,1 7.5,16A1.5,1.5 0 0,1 9,14.5M15,14.5A1.5,1.5 0 0,1 16.5,16A1.5,1.5 0 0,1 15,17.5A1.5,1.5 0 0,1 13.5,16A1.5,1.5 0 0,1 15,14.5Z",
    "mdi:view-dashboard": "M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z",
    "mdi:lightbulb": "M12,2A7,7 0 0,0 5,9C5,11.38 6.19,13.47 8,14.74V17A1,1 0 0,0 9,18H15A1,1 0 0,0 16,17V14.74C17.81,13.47 19,11.38 19,9A7,7 0 0,0 12,2M9,21A1,1 0 0,0 10,22H14A1,1 0 0,0 15,21V20H9V21Z",
    "mdi:thermometer": "M15,13V5A3,3 0 0,0 9,5V13A5,5 0 1,0 15,13M12,4A1,1 0 0,1 13,5V8H11V5A1,1 0 0,1 12,4Z",
    "mdi:cellphone": "M17,19H7V5H17M17,1H7C5.89,1 5,1.89 5,3V21A2,2 0 0,0 7,23H17A2,2 0 0,0 19,21V3C19,1.89 18.1,1 17,1Z",
    "mdi:tablet": "M19,18H5V6H19M21,4H3C1.89,4 1,4.89 1,6V18A2,2 0 0,0 3,20H21A2,2 0 0,0 23,18V6C23,4.89 22.1,4 21,4Z",
    "mdi:monitor": "M21,16H3V4H21M21,2H3C1.89,2 1,2.89 1,4V16A2,2 0 0,0 3,18H10V20H8V22H16V20H14V18H21A2,2 0 0,0 23,16V4C23,2.89 22.1,2 21,2Z",
    "mdi:shield-home": "M11,13H13V16H16V11H18L12,6L6,11H8V16H11V13M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1Z",
    "mdi:cctv": "M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z",
    "mdi:cog": "M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z",
    "mdi:apps": "M16,20H20V16H16M16,14H20V10H16M10,8H14V4H10M16,8H20V4H16M10,14H14V10H10M4,14H8V10H4M4,20H8V16H4M10,20H14V16H10M4,8H8V4H4V8Z",
    "mdi:flash": "M7,2V13H10V22L17,10H13L17,2H7Z",
    "mdi:music": "M21,3V15.5A3.5,3.5 0 0,1 17.5,19A3.5,3.5 0 0,1 14,15.5A3.5,3.5 0 0,1 17.5,12C18.04,12 18.55,12.12 19,12.34V6.47L9,8.6V17.5A3.5,3.5 0 0,1 5.5,21A3.5,3.5 0 0,1 2,17.5A3.5,3.5 0 0,1 5.5,14C6.04,14 6.55,14.12 7,14.34V6L21,3Z",
}

_CMD_OR_NUM_RE = re.compile(
    r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?"
)


def _hex_to_rgba(color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    cleaned = color.lstrip("#")
    if len(cleaned) != 6:
        return (3, 169, 244, alpha)
    return (int(cleaned[0:2], 16), int(cleaned[2:4], 16), int(cleaned[4:6], 16), alpha)


def _svg_arc_points(
    x1: float,
    y1: float,
    rx: float,
    ry: float,
    phi_deg: float,
    large_arc: int,
    sweep: int,
    x2: float,
    y2: float,
) -> list[tuple[float, float]]:
    if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
        return []
    if abs(rx) < 1e-9 or abs(ry) < 1e-9:
        return [(x2, y2)]

    rx = abs(rx)
    ry = abs(ry)
    phi = math.radians(phi_deg % 360.0)
    cos_p, sin_p = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x1 - x2) * 0.5, (y1 - y2) * 0.5
    x1p = cos_p * dx2 + sin_p * dy2
    y1p = -sin_p * dx2 + cos_p * dy2

    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1.0:
        scale = math.sqrt(lam)
        rx *= scale
        ry *= scale

    rx2, ry2 = rx * rx, ry * ry
    x1p2, y1p2 = x1p * x1p, y1p * y1p
    num = max(0.0, rx2 * ry2 - rx2 * y1p2 - ry2 * x1p2)
    den = rx2 * y1p2 + ry2 * x1p2
    factor = math.sqrt(num / den) if den > 1e-12 else 0.0
    if large_arc == sweep:
        factor = -factor

    cxp = factor * (rx * y1p / ry)
    cyp = factor * (-ry * x1p / rx)
    cx = cos_p * cxp - sin_p * cyp + (x1 + x2) * 0.5
    cy = sin_p * cxp + cos_p * cyp + (y1 + y2) * 0.5

    def _angle(ux: float, uy: float, vx: float, vy: float) -> float:
        return math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)

    theta1 = _angle(1.0, 0.0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = _angle(
        (x1p - cxp) / rx,
        (y1p - cyp) / ry,
        (-x1p - cxp) / rx,
        (-y1p - cyp) / ry,
    )
    if sweep == 0 and dtheta > 0:
        dtheta -= 2.0 * math.pi
    elif sweep == 1 and dtheta < 0:
        dtheta += 2.0 * math.pi

    steps = max(8, int(abs(dtheta) / (math.pi / 14.0)) + 1)
    pts: list[tuple[float, float]] = []
    for idx in range(1, steps + 1):
        t = theta1 + dtheta * (idx / steps)
        ct, st = math.cos(t), math.sin(t)
        px = cx + cos_p * rx * ct - sin_p * ry * st
        py = cy + sin_p * rx * ct + cos_p * ry * st
        pts.append((px, py))
    return pts


def _parse_svg_path_subpaths(path_d: str) -> list[list[tuple[float, float]]]:
    tokens = _CMD_OR_NUM_RE.findall(path_d)
    subpaths: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    cx = cy = 0.0
    sx = sy = 0.0
    last_ctrl_c: tuple[float, float] | None = None
    last_ctrl_q: tuple[float, float] | None = None
    cmd = ""
    i = 0

    def _is_cmd(tok: str) -> bool:
        return len(tok) == 1 and tok.isalpha()

    def _read_num() -> float:
        nonlocal i
        val = float(tokens[i])
        i += 1
        return val

    def _read_arc_flag() -> int:
        nonlocal i
        tok = tokens[i]
        if tok in ("0", "1"):
            i += 1
            return int(tok)
        if len(tok) > 1 and tok[0] in ("0", "1"):
            flag = int(tok[0])
            tokens[i] = tok[1:]
            return flag
        i += 1
        return int(float(tok) != 0.0)

    while i < len(tokens):
        if _is_cmd(tokens[i]):
            cmd = tokens[i]
            i += 1
            if cmd in ("Z", "z"):
                if current:
                    if current[-1] != (sx, sy):
                        current.append((sx, sy))
                    subpaths.append(current)
                    current = []
                cx, cy = sx, sy
                last_ctrl_c = last_ctrl_q = None
                continue
        elif not cmd:
            break

        if cmd in ("M", "m"):
            nx, ny = _read_num(), _read_num()
            if cmd == "m":
                nx += cx
                ny += cy
            if current:
                subpaths.append(current)
            current = [(nx, ny)]
            cx, cy = nx, ny
            sx, sy = nx, ny
            cmd = "L" if cmd == "M" else "l"
            last_ctrl_c = last_ctrl_q = None
        elif cmd in ("L", "l"):
            nx, ny = _read_num(), _read_num()
            if cmd == "l":
                nx += cx
                ny += cy
            current.append((nx, ny))
            cx, cy = nx, ny
            last_ctrl_c = last_ctrl_q = None
        elif cmd in ("H", "h"):
            nx = _read_num()
            if cmd == "h":
                nx += cx
            current.append((nx, cy))
            cx = nx
            last_ctrl_c = last_ctrl_q = None
        elif cmd in ("V", "v"):
            ny = _read_num()
            if cmd == "v":
                ny += cy
            current.append((cx, ny))
            cy = ny
            last_ctrl_c = last_ctrl_q = None
        elif cmd in ("C", "c"):
            x1, y1, x2, y2, x, y = (_read_num() for _ in range(6))
            if cmd == "c":
                x1 += cx; y1 += cy; x2 += cx; y2 += cy; x += cx; y += cy
            for step in range(1, 13):
                t = step / 12.0
                mt = 1.0 - t
                px = mt**3 * cx + 3 * mt**2 * t * x1 + 3 * mt * t**2 * x2 + t**3 * x
                py = mt**3 * cy + 3 * mt**2 * t * y1 + 3 * mt * t**2 * y2 + t**3 * y
                current.append((px, py))
            last_ctrl_c = (x2, y2)
            last_ctrl_q = None
            cx, cy = x, y
        elif cmd in ("S", "s"):
            x2, y2, x, y = (_read_num() for _ in range(4))
            if cmd == "s":
                x2 += cx; y2 += cy; x += cx; y += cy
            if last_ctrl_c:
                x1 = 2 * cx - last_ctrl_c[0]
                y1 = 2 * cy - last_ctrl_c[1]
            else:
                x1, y1 = cx, cy
            for step in range(1, 13):
                t = step / 12.0
                mt = 1.0 - t
                px = mt**3 * cx + 3 * mt**2 * t * x1 + 3 * mt * t**2 * x2 + t**3 * x
                py = mt**3 * cy + 3 * mt**2 * t * y1 + 3 * mt * t**2 * y2 + t**3 * y
                current.append((px, py))
            last_ctrl_c = (x2, y2)
            last_ctrl_q = None
            cx, cy = x, y
        elif cmd in ("Q", "q"):
            x1, y1, x, y = (_read_num() for _ in range(4))
            if cmd == "q":
                x1 += cx; y1 += cy; x += cx; y += cy
            for step in range(1, 11):
                t = step / 10.0
                mt = 1.0 - t
                px = mt**2 * cx + 2 * mt * t * x1 + t**2 * x
                py = mt**2 * cy + 2 * mt * t * y1 + t**2 * y
                current.append((px, py))
            last_ctrl_q = (x1, y1)
            last_ctrl_c = None
            cx, cy = x, y
        elif cmd in ("T", "t"):
            x, y = _read_num(), _read_num()
            if cmd == "t":
                x += cx; y += cy
            if last_ctrl_q:
                x1 = 2 * cx - last_ctrl_q[0]
                y1 = 2 * cy - last_ctrl_q[1]
            else:
                x1, y1 = cx, cy
            for step in range(1, 11):
                t = step / 10.0
                mt = 1.0 - t
                px = mt**2 * cx + 2 * mt * t * x1 + t**2 * x
                py = mt**2 * cy + 2 * mt * t * y1 + t**2 * y
                current.append((px, py))
            last_ctrl_q = (x1, y1)
            last_ctrl_c = None
            cx, cy = x, y
        elif cmd in ("A", "a"):
            rx = _read_num()
            ry = _read_num()
            rot = _read_num()
            large_arc = _read_arc_flag()
            sweep = _read_arc_flag()
            x = _read_num()
            y = _read_num()
            if cmd == "a":
                x += cx
                y += cy
            current.extend(_svg_arc_points(cx, cy, rx, ry, rot, large_arc, sweep, x, y))
            cx, cy = x, y
            last_ctrl_c = last_ctrl_q = None
        else:
            break

    if current:
        subpaths.append(current)
    return subpaths


def _rasterize_svg_mask(path_d: str, size: int) -> Image.Image:
    '''Rasterize a 24x24 MDI SVG path onto a grayscale alpha mask using even-odd fill.'''
    subpaths = _parse_svg_path_subpaths(path_d)
    scale = size / 24.0
    edges: list[tuple[float, float, float, float]] = []
    for sp in subpaths:
        if len(sp) < 2:
            continue
        pts = list(sp)
        if pts[-1] != pts[0]:
            pts.append(pts[0])
        for k in range(len(pts) - 1):
            x0, y0 = pts[k][0] * scale, pts[k][1] * scale
            x1, y1 = pts[k + 1][0] * scale, pts[k + 1][1] * scale
            if abs(y0 - y1) > 1e-6:
                edges.append((x0, y0, x1, y1))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    for row in range(size):
        sy = row + 0.5
        xs: list[float] = []
        for x0, y0, x1, y1 in edges:
            if (y0 <= sy < y1) or (y1 <= sy < y0):
                t = (sy - y0) / (y1 - y0)
                xs.append(x0 + t * (x1 - x0))
        xs.sort()
        for idx in range(0, len(xs) - 1, 2):
            lx = max(0, int(round(xs[idx])))
            rx = min(size - 1, int(round(xs[idx + 1])))
            if rx >= lx:
                draw.line([(lx, row), (rx, row)], fill=255)
    return mask


class PillowIconComposer:
    '''Composites HA icons, MDI vector paths, uploads, and corner badges.'''

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._cache: OrderedDict[str, bytes] = OrderedDict()

    async def async_render_png(
        self,
        spec: PwaIconSpec,
        size: int,
        maskable: bool = False,
        cache_key_suffix: str = "",
    ) -> bytes:
        key_payload = json.dumps(
            {"spec": spec.to_dict(), "size": size, "maskable": maskable, "k": cache_key_suffix},
            sort_keys=True,
        )
        cache_key = hashlib.sha256(key_payload.encode("utf-8")).hexdigest()
        if cache_key in self._cache:
            self._cache.move_to_end(cache_key)
            return self._cache[cache_key]

        data = await self._hass.async_add_executor_job(
            self._render_sync, spec, size, maskable
        )
        self._cache[cache_key] = data
        if len(self._cache) > 96:
            self._cache.popitem(last=False)
        return data

    def _render_sync(self, spec: PwaIconSpec, size: int, maskable: bool) -> bytes:
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

        if spec.mode == IconMode.HA_DEFAULT:
            base_img = self._render_ha_logo(size, spec.bg_color)
        elif spec.mode == IconMode.MDI_ICON:
            base_img = self._render_mdi_card(
                size=size,
                mdi_name=spec.mdi_icon,
                svg_path=spec.icon_svg_path,
                fg_hex=spec.icon_color,
                bg_hex=spec.bg_color,
            )
        elif spec.mode == IconMode.DASHBOARD_DEFAULT:
            dash_icon = spec.resolved_dashboard_icon or spec.mdi_icon or "mdi:view-dashboard"
            base_img = self._render_mdi_card(
                size=size,
                mdi_name=dash_icon,
                svg_path=spec.icon_svg_path,
                fg_hex=spec.icon_color,
                bg_hex=spec.bg_color,
            )
        elif spec.mode == IconMode.HA_WITH_BADGE:
            base_img = self._render_ha_logo(size, spec.bg_color)
            badge = self._render_badge(
                badge_size=max(36, int(size * 0.42)),
                is_ha_badge=False,
                mdi_name=spec.badge_icon,
                svg_path=spec.badge_svg_path,
                fg_hex=spec.badge_color,
                bg_hex=spec.badge_bg_color,
            )
            base_img = self._paste_badge(base_img, badge, spec.badge_position)
        elif spec.mode == IconMode.ICON_WITH_HA_BADGE:
            if spec.uploaded_image_b64:
                base_img = self._render_uploaded(size, spec.uploaded_image_b64, spec.bg_color)
            else:
                base_img = self._render_mdi_card(
                    size=size,
                    mdi_name=spec.mdi_icon,
                    svg_path=spec.icon_svg_path,
                    fg_hex=spec.icon_color,
                    bg_hex=spec.bg_color,
                )
            badge = self._render_badge(
                badge_size=max(36, int(size * 0.42)),
                is_ha_badge=True,
                mdi_name="mdi:home-assistant",
                svg_path="",
                fg_hex="#ffffff",
                bg_hex="#03a9f4",
            )
            base_img = self._paste_badge(base_img, badge, spec.badge_position)
        elif spec.mode == IconMode.UPLOADED:
            base_img = self._render_uploaded(size, spec.uploaded_image_b64, spec.bg_color)
        else:
            base_img = self._render_ha_logo(size, spec.bg_color)

        if maskable:
            pad_ratio = max(0.08, spec.maskable_padding_pct / 100.0)
            inner_size = max(16, int(size * (1.0 - 2.0 * pad_ratio)))
            inner = base_img.resize((inner_size, inner_size), _LANCZOS)
            bg_fill = Image.new("RGBA", (size, size), _hex_to_rgba(spec.bg_color, 255))
            offset = (size - inner_size) // 2
            bg_fill.paste(inner, (offset, offset), inner)
            canvas = bg_fill
        else:
            radius = int(size * (spec.corner_radius_pct / 100.0))
            if radius > 0:
                alpha_mask = Image.new("L", (size, size), 0)
                draw = ImageDraw.Draw(alpha_mask)
                draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=255)
                canvas.paste(base_img, (0, 0), alpha_mask)
            else:
                canvas = base_img

        out = io.BytesIO()
        canvas.save(out, format="PNG", optimize=True)
        return out.getvalue()

    def _find_hass_frontend_icon(self) -> Path | None:
        try:
            import hass_frontend  # type: ignore[import-not-found]

            icons_dir = Path(hass_frontend.where()) / "static" / "icons"
            if not icons_dir.is_dir():
                return None
            for name in ("favicon-512x512.png", "favicon-192x192.png", "favicon-apple-180x180.png"):
                candidate = icons_dir / name
                if candidate.is_file():
                    return candidate
            pngs = sorted(icons_dir.glob("favicon-*.png"), reverse=True)
            if pngs:
                return pngs[0]
        except Exception:  # noqa: BLE001
            pass
        return None

    def _render_ha_logo(self, size: int, fallback_bg: str) -> Image.Image:
        ha_path = self._find_hass_frontend_icon()
        if ha_path is not None:
            try:
                with Image.open(ha_path) as img:
                    rgba = img.convert("RGBA")
                    return rgba.resize((size, size), _LANCZOS)
            except Exception as err:  # noqa: BLE001
                _LOGGER.debug("Failed loading hass_frontend icon %s: %s", ha_path, err)

        return self._render_mdi_card(
            size=size,
            mdi_name="mdi:home-assistant",
            svg_path=BUILTIN_MDI_PATHS["mdi:home-assistant"],
            fg_hex="#ffffff",
            bg_hex="#18bcf2" if fallback_bg == "#03a9f4" else fallback_bg,
        )

    def _render_mdi_card(
        self,
        size: int,
        mdi_name: str,
        svg_path: str,
        fg_hex: str,
        bg_hex: str,
    ) -> Image.Image:
        img = Image.new("RGBA", (size, size), _hex_to_rgba(bg_hex, 255))
        path_d = svg_path or BUILTIN_MDI_PATHS.get(mdi_name, "")
        if path_d:
            ss_size = min(256, max(96, int(size * 0.68)))
            mask_hi = _rasterize_svg_mask(path_d, ss_size)
            target_icon_size = max(16, int(size * 0.64))
            mask = mask_hi.resize((target_icon_size, target_icon_size), _LANCZOS)
            fg_layer = Image.new("RGBA", (target_icon_size, target_icon_size), _hex_to_rgba(fg_hex, 255))
            pos = (size - target_icon_size) // 2
            img.paste(fg_layer, (pos, pos), mask)
        else:
            draw = ImageDraw.Draw(img)
            inset = int(size * 0.22)
            draw.rounded_rectangle(
                [(inset, inset), (size - inset, size - inset)],
                radius=max(6, int(size * 0.14)),
                outline=_hex_to_rgba(fg_hex, 255),
                width=max(4, int(size * 0.07)),
            )
            center = size // 2
            dot_r = max(4, int(size * 0.10))
            draw.ellipse(
                [(center - dot_r, center - dot_r), (center + dot_r, center + dot_r)],
                fill=_hex_to_rgba(fg_hex, 255),
            )
        return img

    def _render_uploaded(self, size: int, b64_data: str, bg_hex: str) -> Image.Image:
        if not b64_data:
            return self._render_mdi_card(
                size, "mdi:apps", BUILTIN_MDI_PATHS["mdi:apps"], "#ffffff", bg_hex
            )
        raw_str = b64_data.split(",", 1)[1] if "," in b64_data else b64_data
        try:
            raw_bytes = base64.b64decode(raw_str, validate=True)
            with Image.open(io.BytesIO(raw_bytes)) as src:
                rgba = src.convert("RGBA")
                bg = Image.new("RGBA", (size, size), _hex_to_rgba(bg_hex, 255))
                fitted = rgba.resize((size, size), _LANCZOS)
                bg.paste(fitted, (0, 0), fitted)
                return bg
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("Invalid uploaded icon payload, falling back to default: %s", err)
            return self._render_mdi_card(
                size, "mdi:apps", BUILTIN_MDI_PATHS["mdi:apps"], "#ffffff", bg_hex
            )

    def _render_badge(
        self,
        badge_size: int,
        is_ha_badge: bool,
        mdi_name: str,
        svg_path: str,
        fg_hex: str,
        bg_hex: str,
    ) -> Image.Image:
        badge = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(badge)
        border = max(2, int(badge_size * 0.08))
        draw.ellipse(
            [(0, 0), (badge_size - 1, badge_size - 1)],
            fill=(255, 255, 255, 240),
        )
        draw.ellipse(
            [(border, border), (badge_size - 1 - border, badge_size - 1 - border)],
            fill=_hex_to_rgba(bg_hex, 255),
        )

        inner_size = max(12, badge_size - 2 * border)
        if is_ha_badge:
            inner_logo = self._render_ha_logo(inner_size, bg_hex)
            circle_mask = Image.new("L", (inner_size, inner_size), 0)
            ImageDraw.Draw(circle_mask).ellipse(
                [(0, 0), (inner_size - 1, inner_size - 1)], fill=255
            )
            badge.paste(inner_logo, (border, border), circle_mask)
        else:
            inner_mdi = self._render_mdi_card(
                size=inner_size,
                mdi_name=mdi_name,
                svg_path=svg_path,
                fg_hex=fg_hex,
                bg_hex=bg_hex,
            )
            circle_mask = Image.new("L", (inner_size, inner_size), 0)
            ImageDraw.Draw(circle_mask).ellipse(
                [(0, 0), (inner_size - 1, inner_size - 1)], fill=255
            )
            badge.paste(inner_mdi, (border, border), circle_mask)
        return badge

    @staticmethod
    def _paste_badge(
        base: Image.Image, badge: Image.Image, position: BadgePosition
    ) -> Image.Image:
        w, h = base.size
        bw, bh = badge.size
        margin = max(4, int(w * 0.04))
        if position == BadgePosition.TOP_LEFT:
            xy = (margin, margin)
        elif position == BadgePosition.TOP_RIGHT:
            xy = (w - bw - margin, margin)
        elif position == BadgePosition.BOTTOM_LEFT:
            xy = (margin, h - bh - margin)
        else:
            xy = (w - bw - margin, h - bh - margin)
        out = base.copy()
        out.paste(badge, xy, badge)
        return out
