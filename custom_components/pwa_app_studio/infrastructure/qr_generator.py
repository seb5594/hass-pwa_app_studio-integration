'''Inline SVG QR generator backed by segno.'''

from __future__ import annotations

import io
from homeassistant.core import HomeAssistant


class SegnoQrGenerator:
    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass

    async def async_generate_svg(self, url: str) -> str:
        return await self._hass.async_add_executor_job(self._generate_sync, url)

    @staticmethod
    def _generate_sync(url: str) -> str:
        import segno  # type: ignore[import-not-found]

        qr = segno.make(url, error="m")
        buf = io.BytesIO()
        qr.save(
            buf, kind="svg", border=4, omitsize=True, xmldecl=False,
            dark="#000", light="#fff",
        )
        return buf.getvalue().decode("utf-8")
