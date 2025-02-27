"""Constants for the Envisalink_new integration."""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from homeassistant.const import (
    CONF_CODE,
    CONF_HOST,
    CONF_TIMEOUT,
)

DOMAIN = "envisalink_new"

LOGGER = logging.getLogger(__package__)

CONF_ALARM_NAME = "alarm_name"
CONF_ZONE_SET = "zone_set"
CONF_PARTITION_SET = "partition_set"

CONF_EVL_KEEPALIVE = "keepalive_interval" # OPTION
CONF_EVL_PORT = "port"
CONF_EVL_VERSION = "evl_version"
CONF_PANEL_TYPE = "panel_type"
CONF_PANIC = "panic_type" # OPTION
CONF_PASS = "password"
CONF_USERNAME = "user_name"
CONF_ZONEDUMP_INTERVAL = "zonedump_interval" # OPTION
CONF_CREATE_ZONE_BYPASS_SWITCHES = "create_zone_bypass_switches" # OPTION
CONF_HONEYWELL_ARM_NIGHT_MODE = "honeywell_arm_night_mode" # OPTION


# Config items used only in the YAML config
CONF_ZONENAME = "name"
CONF_ZONES = "zones"
CONF_ZONETYPE = "type"
CONF_PARTITIONNAME = "name"
CONF_PARTITIONS = "partitions"

# Temporary config entry key used to store values from the YAML config that will transition
# into the ConfigEntry options
CONF_YAML_OPTIONS = "yaml_options"

HONEYWELL_ARM_MODE_INSTANT_LABEL = "Instant"
HONEYWELL_ARM_MODE_INSTANT_VALUE = "7"
HONEYWELL_ARM_MODE_NIGHT_LABEL = "Night Stay"
HONEYWELL_ARM_MODE_NIGHT_VALUE = "33"

DEFAULT_ALARM_NAME = "Alarm"
DEFAULT_CREATE_ZONE_BYPASS_SWITCHES = False
DEFAULT_EVL_VERSION = 4
DEFAULT_KEEPALIVE = 60
DEFAULT_ZONE_SET = ""
DEFAULT_PARTITION_SET = "1"
DEFAULT_PANIC = "Police"
DEFAULT_PORT = 4025
DEFAULT_TIMEOUT = 10
DEFAULT_USERNAME = "user"
DEFAULT_ZONEDUMP_INTERVAL = 30
DEFAULT_ZONETYPE = BinarySensorDeviceClass.OPENING
DEFAULT_HONEYWELL_ARM_NIGHT_MODE = HONEYWELL_ARM_MODE_NIGHT_VALUE

