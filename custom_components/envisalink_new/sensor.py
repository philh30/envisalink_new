"""Support for Envisalink sensors (shows panel info)."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .pyenvisalink.const import STATE_CHANGE_PARTITION

from .const import (
    DOMAIN,
    LOGGER,
    CONF_PARTITIONNAME,
    CONF_PARTITIONS,
    CONF_PARTITION_SET,
    DEFAULT_PARTITION_SET,
)

from .models import EnvisalinkDevice
from .helpers import find_yaml_partition_info, parse_range_string


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    controller = hass.data[DOMAIN][entry.entry_id]

    partition_spec = entry.options.get(CONF_PARTITION_SET)
    partition_set = parse_range_string(partition_spec, min_val=1, max_val=controller.controller.max_partitions)
    partition_info = entry.data.get(CONF_PARTITIONS)
    if partition_set is not None:
        entities = []
        for part_num in partition_set:
            part_entry = find_yaml_partition_info(part_num, partition_info)

            entity = EnvisalinkSensor(
                hass,
                part_num,
                part_entry,
                controller,
            )
            entities.append(entity)

        async_add_entities(entities)




class EnvisalinkSensor(EnvisalinkDevice, SensorEntity):
    """Representation of an Envisalink keypad."""

    def __init__(self, hass, partition_number, partition_info, controller):
        """Initialize the sensor."""
        self._icon = "mdi:alarm"
        self._partition_number = partition_number
        name = f"Partition {partition_number} Keypad"
        self._attr_unique_id = f"{controller.unique_id}_{name}"

        self._attr_has_entity_name = True
        if partition_info:
            # Override the name if there is info from the YAML configuration
            if CONF_PARTITIONNAME in partition_info:
                name = f"{partition_info[CONF_PARTITIONNAME]} Keypad"
                self._attr_has_entity_name = False

        LOGGER.debug("Setting up sensor for partition: %s", name)
        super().__init__(name, controller, STATE_CHANGE_PARTITION, partition_number)

    @property
    def _info(self):
        return self._controller.controller.alarm_state["partition"][self._partition_number]

    @property
    def icon(self):
        """Return the icon if any."""
        return self._icon

    @property
    def native_value(self):
        """Return the overall state."""
        return self._info["status"]["alpha"]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._info["status"]

