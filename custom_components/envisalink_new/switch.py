"""Support for Envisalink zone bypass switches."""
from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .config_flow import find_yaml_zone_info, parse_range_string
from .models import EnvisalinkDevice
from .const import (
    CONF_CREATE_ZONE_BYPASS_SWITCHES,
    CONF_ZONENAME,
    CONF_ZONES,
    CONF_ZONE_SET,
    DOMAIN,
    LOGGER,
    STATE_UPDATE_TYPE_ZONE_BYPASS,
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    controller = hass.data[DOMAIN][entry.entry_id]

    create_bypass_switches = entry.options.get(CONF_CREATE_ZONE_BYPASS_SWITCHES)
    if create_bypass_switches:
        zone_spec = entry.options.get(CONF_ZONE_SET)
        zone_set = parse_range_string(zone_spec, min_val=1, max_val=controller.controller.max_zones)
        zone_info = entry.data.get(CONF_ZONES)
        if zone_set is not None:
            entities = []
            for zone_num in zone_set:
                zone_entry = find_yaml_zone_info(zone_num, zone_info)

                entity = EnvisalinkSwitch(
                    hass,
                    zone_num,
                    zone_entry,
                    controller,
                )
                entities.append(entity)

            async_add_entities(entities)


class EnvisalinkSwitch(EnvisalinkDevice, SwitchEntity):
    """Representation of an Envisalink switch."""

    def __init__(self, hass, zone_number, zone_info, controller):
        """Initialize the switch."""
        self._zone_number = zone_number
        name = "Bypass"
        self._attr_unique_id = f"{controller.unique_id}_Zone {zone_number} Bypass"
        self._attr_has_entity_name = True

        LOGGER.debug(f"Setting up zone bypass switch: {zone_number}")
        super().__init__(name, controller, STATE_UPDATE_TYPE_ZONE_BYPASS, zone_number)
        self._attr_device_info = {
            'identifiers': {(DOMAIN, f"{controller.unique_id}_Zone {zone_number}")},
            'name': f"{self._controller.controller.panel_type} Zone {zone_number}",
            'manufacturer':'eyezon',
            'model': f'Envisalink {self._controller.controller.envisalink_version}: {self._controller.controller.panel_type} Zone',
            'sw_version': self._controller.controller.firmware_version,
            'hw_version': self._controller.controller.envisalink_version,
            'configuration_url': f"http://{self._controller.controller.host}",
            }
        if zone_info:
            # Override the name and type if there is info from the YAML configuration
            if CONF_ZONENAME in zone_info:
                self._attr_device_info['name'] = zone_info[CONF_ZONENAME]

    @property
    def _info(self):
        return self._controller.controller.alarm_state["zone"][self._zone_number]

    @property
    def is_on(self):
        """Return the boolean response if the zone is bypassed."""
        return self._info["bypassed"]

    async def async_turn_on(self, **kwargs):
        """Send the bypass keypress sequence to toggle the zone bypass."""
        await self._controller.controller.toggle_zone_bypass(self._zone_number)

    async def async_turn_off(self, **kwargs):
        """Send the bypass keypress sequence to toggle the zone bypass."""
        await self._controller.controller.toggle_zone_bypass(self._zone_number)

