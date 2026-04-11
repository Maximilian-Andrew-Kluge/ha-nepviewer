"""Sensor entities for NEPViewer Solar."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfMass, UnitOfLength, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NEPViewerCoordinator


@dataclass(frozen=True)
class NEPViewerSensorDescription(SensorEntityDescription):
    """Describes a NEPViewer sensor."""
    data_key: str = ""


SENSOR_TYPES: tuple[NEPViewerSensorDescription, ...] = (
    NEPViewerSensorDescription(
        key="current_power",
        data_key="current_power_w",
        name="Aktuelle Leistung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
    ),
    NEPViewerSensorDescription(
        key="today_energy",
        data_key="today_kwh",
        name="Ertrag heute",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:weather-sunny",
    ),
    NEPViewerSensorDescription(
        key="month_energy",
        data_key="month_kwh",
        name="Ertrag diesen Monat",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:calendar-month",
    ),
    NEPViewerSensorDescription(
        key="year_energy",
        data_key="year_kwh",
        name="Ertrag dieses Jahr",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:calendar",
    ),
    NEPViewerSensorDescription(
        key="total_energy",
        data_key="total_kwh",
        name="Gesamtertrag",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:sigma",
    ),
    NEPViewerSensorDescription(
        key="co2_saved",
        data_key="co2_saved_kg",
        name="CO₂ eingespart",
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:molecule-co2",
    ),
    NEPViewerSensorDescription(
        key="trees_saved",
        data_key="trees_saved",
        name="Bäume gepflanzt (Äquivalent)",
        native_unit_of_measurement="Bäume",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:tree",
    ),
    NEPViewerSensorDescription(
        key="km_driven",
        data_key="km_driven",
        name="Autofahrt eingespart",
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:car-electric",
    ),
    NEPViewerSensorDescription(
        key="hours_powered",
        data_key="hours_powered",
        name="Haushalt versorgt",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:home-lightning-bolt",
    ),
    NEPViewerSensorDescription(
        key="oil_saved_bbl",
        data_key="oil_saved_bbl",
        name="Öl eingespart",
        native_unit_of_measurement="BBL",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:oil",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NEPViewer sensors from config entry."""
    coordinator: NEPViewerCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        NEPViewerSensor(coordinator, description, entry)
        for description in SENSOR_TYPES
    )


class NEPViewerSensor(CoordinatorEntity[NEPViewerCoordinator], SensorEntity):
    """A sensor that reads from the NEPViewer coordinator."""

    entity_description: NEPViewerSensorDescription

    def __init__(
        self,
        coordinator: NEPViewerCoordinator,
        description: NEPViewerSensorDescription,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.data['plant_id']}_{description.key}"
        self._attr_has_entity_name = True

        plant_id = entry.data["plant_id"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, plant_id)},
            name=coordinator.data.get("plant_name") or f"Solar {plant_id}",
            manufacturer="Northern Electric & Power (NEP)",
            model="Micro Inverter",
            configuration_url=f"https://user.nepviewer.com/pvPlant/detail?id={plant_id}",
        )

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        return self.coordinator.data.get(self.entity_description.data_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        return {
            "plant_id": self.coordinator.api._plant_id,
            "plant_status": self.coordinator.data.get("plant_status", "unknown"),
        }
