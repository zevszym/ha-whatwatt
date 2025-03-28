"""Button platform for WhatWatt integration."""
import logging
import webbrowser
from typing import Any, Callable, Dict, Optional

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_IP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the WhatWatt button."""
    device_ip = config_entry.data.get(CONF_DEVICE_IP)
    device_info = hass.data[DOMAIN][config_entry.entry_id]["device_info"]
    
    async_add_entities([WhatWattConfigButton(device_ip, device_info)])


class WhatWattConfigButton(ButtonEntity):
    """Button to open the WhatWatt configuration page."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:cog"
    
    def __init__(self, device_ip: str, device_info: Dict[str, Any]) -> None:
        """Initialize the button entity."""
        self._device_ip = device_ip
        self._device_info = device_info
        self._attr_unique_id = f"{device_info['identifiers']}_config"
        self._attr_name = f"{device_info['name']} Configuration"
        self._attr_device_info = device_info

    def press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug("Opening WhatWatt configuration page at http://%s", self._device_ip)
        
        # Open the configuration page in the default web browser
        # Note: This will only work if Home Assistant is running on a system with a GUI
        # For other systems, this will log an error but not crash
        try:
            webbrowser.open(f"http://{self._device_ip}")
        except Exception as ex:
            _LOGGER.error("Failed to open configuration page: %s", ex)
