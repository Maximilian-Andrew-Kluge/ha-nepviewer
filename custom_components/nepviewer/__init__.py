"""NEPViewer Solar – Home Assistant Custom Integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .api import NEPViewerAPI
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .coordinator import NEPViewerCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NEPViewer from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]
    plant_id = entry.data["plant_id"]
    scan_interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)

    api = NEPViewerAPI(email, password, plant_id)

    # Try to login once at startup to surface errors early
    if not await api.async_login():
        raise ConfigEntryNotReady("Could not log in to NEPViewer at startup")

    coordinator = NEPViewerCoordinator(hass, api, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update (e.g. scan interval changed)."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload NEPViewer config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: NEPViewerCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.api.async_close()
    return unload_ok
