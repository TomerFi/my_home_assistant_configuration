"""**********************************************************************************************
 * Home Assistant Bridge (Current Version: 20180512)
 * *************************************************
 * Created by Tomer Figenblat
 * GitHub: https://github.com/TomerFi
 * YouTube: https://www.youtube.com/channel/UCH9z4dabjTo-pRqM3_i5RTg
 * Linkedin: https://www.linkedin.com/in/tomer-figenblat-18aabb76/
 *
 * This custom component allows bridging devices from Smartthings to Home Assistant.
 * This is not a "standalone" custom component, A designated Smartthings smartapp is required.
 * You can find all the required files and documentation in the project's github repository:
 * https://github.com/TomerFi/home_assistant_smartthings_bridge
 *
 * This project is a work in progress, so please follow the github repository for future updates.
 * Tested contributions to this project will be gladly accepted via the repository.
 * If any error occurs, please open an issue with the appropriate information and log details.
 *
 * This project currently supports creating Smartthings devices as sensor entities.
 * Therefore this script, which actually represents the bridge connections to st, is not enough.
 * You also need to make use of the platform scripts, which represents the ha entities.
 *
 * This script should be placed in '/custom_components/smartthings_bridge/__init__.py'.
 * The platform, for example the sensor platform, should be places in '/custom_components/sensor/smartthings_bridge.py'.
 *
 * You only need to configure the component as such:
 * 
 * smartthings_bridge:
 *   url: place_your_smartapp_api_url_here
 *   token: place_your_smartapp_access_token_here
 *
 * For troubleshooting purposes, you can set the component's/platform's log level to debug:
 *   custom_components.smartthings_bridge: debug
 *
 *********************************************************************************************"""

import asyncio
import logging
import requests
import traceback
import datetime

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.core import callback
from homeassistant.const import (CONF_URL, CONF_TOKEN, CONF_SCAN_INTERVAL, EVENT_HOMEASSISTANT_STOP, EVENT_HOMEASSISTANT_CLOSE)
from homeassistant.helpers.discovery import (async_load_platform, async_listen_platform)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.components.persistent_notification import (DOMAIN as PERSISTANT_DOMAIN, ATTR_MESSAGE, ATTR_TITLE, SERVICE_CREATE)


_LOGGER = logging.getLogger(__name__)

#############################
#### Component Constants ####
#############################
DOMAIN = "smartthings_bridge"
ENTITY_PREFIX = "st_bridge_{}"
DEFAULT_SCAN_INTERVAL = datetime.timedelta(minutes=5)
KEY_DEVICES = "devices"
KEY_ST_URL = "st_url"
KEY_ST_HEADERS = "st_headers"

ONE_VALUE_SENSOR_ATTRIBUTES = ["acceleration", "airQuality", "carbonDioxide", "contact", "illuminance",
     "motion", "odorLevel", "presence", "sleeping", "smoke", "sound", "temperature", "touch", "water"]

DUST_SENSOR_ATTRIBUTES = ["fineDustLevel", "dustLevel"]

STEP_SENSOR_ATTRIBUTES = ["goal", "steps"]

###########################
#### Device Attributes ####
###########################
ATTR_HA_TYPE= "ha_type"
ATTR_DEVICE_ID = "device_id"
ATTR_DEVICE_TYPE = "device_type"
ATTR_HUB_NAME = "hub_name"
ATTR_LAST_CHANGE = "last_changed"
ATTR_MODEL_NAME = "model_name"
ATTR_MANUFACTURER_NAME = "manufacturer_name"
ATTR_ID = "id"
ATTR_LABEL = "label"
ATTR_DISPLAY_NAME = "display_name"
ATTR_STATUS = "status"
ATTR_TYPE_NAME = "type_name"
ATTR_WATCHED_ATTRIBUTES = "watched_attributes"

##############################
#### Bridge Mappings Dict ####
##############################
MAPPINGS = {
    "start_bridge": "/start_bridge",
    "stop_bridge": "/stop_bridge",
    "check_bridge": "/check_bridge",
    "get_devices": "/get_devices"
}

#######################
#### Custom Events ####
#######################
EVENT_SMARTAPP_UNINSTALLED = "st_smartapp_uninstalled"
EVENT_DEVICE_UPDATE = "st_bridge_device_update"

###############################
#### Configuration Schemas ####
###############################
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_URL): cv.url,
        vol.Required(CONF_TOKEN): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_timedelta
        })
}, extra=vol.ALLOW_EXTRA)

###################################
#### Bridge callback functions ####
###################################
@callback
def get_last_changed(timestamps_list):
    """get the highst datetime as datetime from a list of timestamps"""
    datetime_list = []
    for str_ts in timestamps_list:
        datetime_list.append(datetime.datetime.strptime(str_ts, "%Y-%m-%dT%H:%M:%S.%fZ"))

    return max(datetime_list)


@callback
def parse_capability_values(attributes):
    """parse entity state from capablity attributes"""
    for attribute, data in attributes.items():
        if attribute in ONE_VALUE_SENSOR_ATTRIBUTES:
            return data["value"], data["last_changed"]
        elif attribute in DUST_SENSOR_ATTRIBUTES:
            state = str(attributes["fineDustLevel"]["value"]) + "-" + str(attributes["dustLevel"]["value"])
            last_changed = get_last_changed([str(attributes["fineDustLevel"]["last_changed"]), str(attributes["dustLevel"]["last_changed"])])
            return state, last_changed
        elif attribute in STEP_SENSOR_ATTRIBUTES:
            state = str(attributes["steps"]["value"]) + "/" + str(attributes["goal"]["value"])
            last_changed = get_last_changed([str(attributes["steps"]["last_changed"]), str(attributes["goal"]["last_changed"])])
            return state, last_changed
        else:
            return None, None


@callback
def send_st_api_requests(url, mapping, headers):
    """יsend http requests to the smartthings smartapp api"""
    response = None
    try:
        response = requests.get(url=url + mapping, headers=headers).json()
    except:
        _LOGGER.exception("smartthings api request caught exception: " + traceback.format_exc())
        return None

    if response is None:
        _LOGGER.error("smartthings api request isn't responding")
        return None

    if "error" in response:
        _LOGGER.error("smartthings api returned error: " + response["message"])
        return None

    return response

#########################
#### Component Setup ####
#########################
@asyncio.coroutine
def async_setup(hass, config):
    _LOGGER.info("starting component setup")
    """יget the configuration"""
    st_url = config[DOMAIN][CONF_URL]
    st_token = config[DOMAIN][CONF_TOKEN]
    update_interval = config[DOMAIN][CONF_SCAN_INTERVAL]

    st_headers = {
        "Authorization": "Bearer " + st_token
    }

    #########################
    #### Events Handlers ####
    #########################
    @callback
    def stop_bridge_callback(evt):
        """יcallback for shutting down the bridge and homeassistant stop event if launched"""
        _LOGGER.info("stopping the bridge")
        stop_bridge = send_st_api_requests(st_url, MAPPINGS["stop_bridge"], st_headers)
        if stop_bridge is None:
            _LOGGER.error("smartthings bridge failed to stop")
            return
        if stop_bridge["status"]:
            _LOGGER.info(stop_bridge["message"])
        else:
            _LOGGER.error(stop_bridge["message"])


    @callback
    def smartapp_uninstalled_callback(evt):
        """יcallback for notifying the user when the smartapp is unistalled"""
        _LOGGER.error("the bridge smartapp was just uninstalled from your device, please update the url and token after reinstalling and restart")
        notification = {
            ATTR_TITLE: "Smartthings SmartApp uninstalled",
            ATTR_MESSAGE: "Please update the url and token after reinstalling and restart"
        }
        hass.async_add_job(hass.services.async_call(PERSISTANT_DOMAIN, SERVICE_CREATE, notification))

    #########################
    #### Scheduled Calls ####
    #########################
    @asyncio.coroutine
    def async_request_devices_update_callback(evt):
        """function to be called in intervals from the event loop an request devices update from the bridge"""
        _LOGGER.debug("requesting devices update from bridge")
        devices_details = send_st_api_requests(st_url, MAPPINGS["get_devices"], st_headers)
        
        if devices_details is None:
            _LOGGER.error("smartthings bridge did not return any devices")
            return

        for device_det in devices_details:
            hass.bus.async_fire(EVENT_DEVICE_UPDATE, device_det)

    ############################
    #### Platforms Discover ####
    ############################
    @asyncio.coroutine
    def async_paltform_discoverd(paltform, discovery_info=None):
        if paltform == DOMAIN:
            """check and start the bridge when any of the platforms was discoverd"""
            _LOGGER.info("platform discoverd, starting bridge")
            bridge_status = send_st_api_requests(st_url, MAPPINGS["check_bridge"], st_headers)

            if bridge_status is None:
                _LOGGER.error("smartthings bridge is not responding")
                return

            if bridge_status["status"]:
                _LOGGER.info(bridge_status["message"])
            else:
                start_bridge = send_st_api_requests(st_url, MAPPINGS["start_bridge"], st_headers)

                if start_bridge is None:
                    _LOGGER.error("smartthings bridge failed to start")
                    return
                if start_bridge["status"]:
                    _LOGGER.info(start_bridge["message"])
                else:
                    _LOGGER.error(start_bridge["message"])

            """register to homeassistant stop event"""
            hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_bridge_callback)
            _LOGGER.debug("registerd to " + EVENT_HOMEASSISTANT_STOP + " event")
            
            """schedule track time interval for requesting device updates from the bridge"""
            async_track_time_interval(hass, async_request_devices_update_callback, update_interval)
            _LOGGER.debug("update request interval is set to " + str(update_interval))

    
    """יget devices from smartthings"""
    response = send_st_api_requests(st_url, MAPPINGS["get_devices"], st_headers)
    if response is None:
        _LOGGER.error("smartthings bridge did not return any devices")
        return False
    _LOGGER.debug("discoverd " + str(len(response)) + " devices")

    """create domain lists from devices list"""
    sensor_devices = []
    switch_devices = []
    for device in response:
        if device[ATTR_HA_TYPE] == SENSOR_DOMAIN:
            sensor_devices.append(device)
        if device[ATTR_HA_TYPE] == SWITCH_DOMAIN:
            switch_devices.append(device)
    
    tasks = {}
    if sensor_devices:
        _LOGGER.debug("found " + str(len(sensor_devices)) + " " + SENSOR_DOMAIN + " devices")
        tasks[SENSOR_DOMAIN] = sensor_devices

    if switch_devices:
        _LOGGER.debug("found " + str(len(switch_devices)) + " " + SWITCH_DOMAIN + " devices")
        tasks[SWITCH_DOMAIN] = switch_devices

    """load platforms based on devices types"""
    if tasks:
        for component, entities in tasks.items():
            _LOGGER.info("discovering " + str(len(tasks)) + " platforms")
            async_listen_platform(hass, component, async_paltform_discoverd)
            hass.async_add_job(async_load_platform(hass, component, DOMAIN, {KEY_ST_URL: st_url, KEY_ST_HEADERS: st_headers, KEY_DEVICES: entities}, config))

        """register to event launched when the smartapp is uninstalled"""
        hass.bus.async_listen_once(EVENT_SMARTAPP_UNINSTALLED, smartapp_uninstalled_callback)
        _LOGGER.debug("registerd to " + EVENT_SMARTAPP_UNINSTALLED + " event")
        return True
    else:
        _LOGGER.error("smartthings bridge did not return any eligble devices, please make sure you configured the smartapp with authorized devices")
        return False

    

#########################################
#### Representation of the ST Device ####
#########################################
class ST_Device(object):
    def __init__(self, device_dict):
        """initialize the object"""
        self._id = device_dict[ATTR_ID]
        self._label = device_dict[ATTR_LABEL]
        self._hub_name = device_dict[ATTR_HUB_NAME] if ATTR_HUB_NAME in device_dict else None
        self._display_name = device_dict[ATTR_DISPLAY_NAME]
        self._manufacturer_name = device_dict[ATTR_MANUFACTURER_NAME] if ATTR_MANUFACTURER_NAME in device_dict else None
        self._model_name = device_dict[ATTR_MODEL_NAME] if ATTR_MODEL_NAME in device_dict else None
        self._status = device_dict[ATTR_STATUS]
        self._type_name = device_dict[ATTR_TYPE_NAME]
        self._watched_attributes = device_dict[ATTR_WATCHED_ATTRIBUTES]

    @property
    def id(self):
        """return the st device id"""
        return self._id

    @property
    def label(self):
        """return the st device label"""
        return self._label

    @property
    def hub_name(self):
        """return the st hub name for the device"""
        return self._hub_name if self._hub_name != "null" else None

    @property
    def display_name(self):
        """return the st device display name"""
        return self._display_name

    @property
    def manufacturer_name(self):
        """return the st device manufacturer name"""
        return self._manufacturer_name if self._manufacturer_name != "null" else None

    @property
    def model_name(self):
        """return the st device model name"""
        return self._model_name if self._model_name != "null" else None

    @property
    def status(self):
        """return the st device status"""
        return self._status

    @property
    def type_name(self):
        """return the st device type name"""
        return self._type_name

    @property
    def watched_attributes(self):
        """return the watched attributes by the bridge"""
        return self._watched_attributes
