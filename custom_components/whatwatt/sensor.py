"""Sensor platform for WhatWatt integration."""
import logging
import json
from typing import Any, Callable, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import slugify

from .const import (
    DOMAIN,
    ATTR_SYS_ID,
    ATTR_METER_ID,
    ATTR_TIME,
    ATTR_POWER_IN,
    ATTR_POWER_OUT,
    ATTR_ENERGY_IN,
    ATTR_ENERGY_OUT,
    ATTR_VOLTAGE_L1,
    ATTR_VOLTAGE_L2,
    ATTR_VOLTAGE_L3,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the WhatWatt sensor platform."""
    # Get the device info from the entry data
    device_info = hass.data[DOMAIN][config_entry.entry_id]["device_info"]
    
    # Create sensors for each sensor type
    sensors = []
    for sensor_type in SENSOR_TYPES:
        sensors.append(
            WhatWattSensor(
                device_info,
                sensor_type,
                SENSOR_TYPES[sensor_type],
            )
        )
    
    async_add_entities(sensors)


class WhatWattSensor(SensorEntity):
    """Representation of a WhatWatt sensor."""

    def __init__(
        self,
        device_info: Dict[str, Any],
        sensor_type: str,
        sensor_config: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        self._device_info = device_info
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        self._state = None
        self._available = False
        
        # Set entity attributes
        self._attr_name = f"{device_info['name']} {sensor_config['name']}"
        self._attr_unique_id = f"{device_info['identifiers']}_{sensor_type}"
        self._attr_device_info = device_info
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        self._attr_icon = sensor_config["icon"]
        self._attr_device_class = sensor_config["device_class"]
        self._attr_state_class = sensor_config["state_class"]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @callback
    def handle_mqtt_message(self, message: Dict[str, Any]) -> None:
        """Handle new MQTT messages."""
        if self._sensor_type in message:
            try:
                # Try to convert the value to float
                self._state = float(message[self._sensor_type])
                self._available = True
            except (ValueError, TypeError) as ex:
                _LOGGER.error(
                    "Could not parse %s value %s: %s",
                    self._sensor_type,
                    message[self._sensor_type],
                    ex,
                )
                self._available = False
            
            # Schedule update
            self.async_write_ha_state()
