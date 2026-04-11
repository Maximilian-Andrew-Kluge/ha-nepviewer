"""DataUpdateCoordinator for NEPViewer."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NEPViewerAPI
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NEPViewerCoordinator(DataUpdateCoordinator):
    """Fetches data from NEPViewer every N seconds."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: NEPViewerAPI,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch latest data from NEPViewer."""
        raw = await self.api.async_get_overview()
        if raw is None:
            raise UpdateFailed("Could not retrieve data from NEPViewer")

        data = raw.get("data", {})
        energy = data.get("energy", {}).get("PVPanel", {})
        stats = data.get("statisticsProduction", {})
        env = data.get("benefit", {})

        return {
            "current_power_w":   float(energy.get("power", 0)),
            "today_kwh":         float(stats.get("today", 0)),
            "month_kwh":         float(stats.get("month", 0)),
            "year_kwh":          float(stats.get("year", 0)),
            "total_kwh":         float(stats.get("total", 0)),
            # Umweltnutzen
            "co2_saved_kg":      float(env.get("co2", 0)),
            "trees_saved":       float(env.get("tree", 0)),
            "km_driven":         float(env.get("car", 0)),
            "hours_powered":     float(env.get("light", 0)),
            "oil_saved_bbl":     float(env.get("oil", 0)),
            "plant_name":        data.get("selected", {}).get("siteName") or data.get("plantName", ""),
            "plant_status":      data.get("statusTitle", str(data.get("status", "unknown"))),
        }
