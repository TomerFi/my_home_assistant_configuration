"""**********************************************************************************************
 * Home Assistant Bridge (Current Version: 20180512)
 * *************************************************
 * Created by Tomer Figenblat
 * GitHub: https://github.com/TomerFi
 * YouTube: https://www.youtube.com/channel/UCH9z4dabjTo-pRqM3_i5RTg
 * Linkedin: https://www.linkedin.com/in/tomer-figenblat-18aabb76/
 *
 * This is a sensor platform for the smartthings_bridge custom component.
 * Used for creating sensor entities to represent Smartthings sensors.
 
 * You can find all the required files and documentation in the project's github repository:
 * https://github.com/TomerFi/home_assistant_smartthings_bridge
 *
 * This project is a work in progress, so please follow the github repository for future updates.
 * Tested contributions to this project will be gladly accepted via the repository.
 * If any error occurs, please open an issue with the appropriate information and log details.
 *
 * This script is a sensor platform and should be placed in
 *   '/custom_components/sensor/smartthings_bridge.py'
 *
 * No configuration is requierd for the platform, please configure the main component appropriately
 * 
 * For troubleshooting purposes, you can set the component's/platform's log level to debug:
 *   custom_components.sensor.smartthings_bridge: debug
 *
 *********************************************************************************************"""

import asyncio
import logging
import traceback

from homeassistant.helpers.entity import (Entity, async_generate_entity_id)
from homeassistant.components.sensor import DOMAIN

from custom_components.smartthings_bridge import (ENTITY_PREFIX, ST_Device, parse_capability_values, EVENT_DEVICE_UPDATE,
    ATTR_DEVICE_ID, ATTR_DEVICE_TYPE, ATTR_HUB_NAME, ATTR_LAST_CHANGE, ATTR_MODEL_NAME, ATTR_MANUFACTURER_NAME,
    KEY_DEVICES, KEY_ST_URL, KEY_ST_HEADERS)

_LOGGER = logging.getLogger(__name__)

############################
#### Platform Constants ####
############################
ENTITY_ID_FORMAT = DOMAIN + "." + ENTITY_PREFIX

########################
#### Platform Setup ####
########################
@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info):
    _LOGGER.info("starting platform setup")
    st_url = discovery_info[KEY_ST_URL]
    st_headers = discovery_info[KEY_ST_HEADERS]

    _LOGGER.debug("adding " + str(len(discovery_info[KEY_DEVICES])) + " devices")

    sensors = []
    for device in discovery_info[KEY_DEVICES]:
        sensors.append(ST_Sensor(hass, st_url, st_headers, (ST_Device(device))))

    if sensors:
        async_add_devices(sensors)

    return True


##############################
#### Sensor Represntation ####
##############################
class ST_Sensor(Entity):
    def __init__(self, hass, st_url, st_headers, st_device):
        """initiate the sensor entity"""
        self._hass = hass
        self.entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, st_device.label, hass=hass)
        self._device = st_device
        self._st_url = st_url
        self._st_headers = st_headers
        self._state, self._last_changed = parse_capability_values(self._device.watched_attributes)
        _LOGGER.debug(self.entity_id + " initialized with state " + str(self._state))
        
        """listen for state changes events"""
        hass.bus.async_listen(EVENT_DEVICE_UPDATE, self.async_device_update)
        _LOGGER.debug(self.entity_id + " registerd to " + EVENT_DEVICE_UPDATE + " events")

    @property
    def name(self):
        """return the friendly name of the entity"""
        return self._device.display_name

    @property
    def should_poll(self):
        """entity should not be polled for state updates"""
        return False

    @property
    def state(self):
        """return the state of the entity"""
        return self._state

    @property
    def device_state_attributes(self):
        """return the state attributes of the entity"""
        attribs = {
            ATTR_DEVICE_ID: self._device.id,
            ATTR_DEVICE_TYPE: self._device.type_name,
            ATTR_LAST_CHANGE: self._last_changed,
        }
        if self._device.hub_name:
            attribs[ATTR_HUB_NAME] = self._device.hub_name
        if self._device.model_name:
            attribs[ATTR_MODEL_NAME] = self._device.model_name
        if self._device.manufacturer_name:
            attribs[ATTR_MANUFACTURER_NAME] = self._device.manufacturer_name

        return attribs

    @asyncio.coroutine
    def async_device_update(self, evt):
        """handles state change events"""
        evt_device = ST_Device(evt.data)
        if evt_device.id == self._device.id:
            _LOGGER.debug(self.entity_id + " received update")
            self._device = evt_device
            self._state, self._last_changed = parse_capability_values(self._device.watched_attributes)
            yield from self.async_update_ha_state()
