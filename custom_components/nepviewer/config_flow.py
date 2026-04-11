"""Config flow for NEPViewer Solar integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .api import NEPViewerAPI
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("email"): str,
        vol.Required("password"): str,
        vol.Required("plant_id"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate credentials by trying to log in."""
    api = NEPViewerAPI(data["email"], data["password"], data["plant_id"])
    try:
        success = await api.async_login()
        if not success:
            raise InvalidAuth
        overview = await api.async_get_overview()
        if overview is None:
            raise CannotConnect
    finally:
        await api.async_close()

    plant_name = (
        overview.get("data", {}).get("plantName")
        or data["plant_id"]
    )
    return {"title": f"NEPViewer – {plant_name}"}


class NEPViewerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for NEPViewer."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            # Prevent duplicate entries for the same plant
            await self.async_set_unique_id(user_input["plant_id"])
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected error during NEPViewer setup")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return NEPViewerOptionsFlow(config_entry)


class NEPViewerOptionsFlow(config_entries.OptionsFlow):
    """Handle options (scan interval)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self._config_entry.options.get(
            "scan_interval", DEFAULT_SCAN_INTERVAL
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("scan_interval", default=current_interval): vol.All(
                        cv.positive_int, vol.Range(min=30, max=3600)
                    )
                }
            ),
        )


class InvalidAuth(Exception):
    """Raised when authentication fails."""


class CannotConnect(Exception):
    """Raised when connection fails."""
