"""Home Assistant Custom Component, Broadlink S1C sensor entity.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

Example:
  .. code-block:: yaml

        sensor:
          - platform: broadlink_s1c
            ip_address: "192.168.0.102"
            mac: "AB:C1:D2:EF:GH:34"
            timeout: 10

"""
# fmt: off
import asyncio
import binascii
import datetime
import logging
import socket
import threading
import traceback
from typing import Callable, Dict, Generator, Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from broadlink import S1C
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_IP_ADDRESS, CONF_MAC, CONF_TIMEOUT,
                                 EVENT_HOMEASSISTANT_STOP,
                                 STATE_ALARM_ARMED_AWAY,
                                 STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED,
                                 STATE_CLOSED, STATE_OPEN, STATE_UNKNOWN)
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.util.dt import now

# fmt: on

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sensor"
ENTITY_ID_FORMAT = DOMAIN + ".broadlink_s1c_{}"
DEFAULT_TIMEOUT = 10

STATE_NO_MOTION = "no_motion"
STATE_MOTION_DETECTED = "motion_detected"
STATE_TAMPERED = "tampered"
STATE_ALARM_SOS = "sos"

UPDATE_EVENT = "BROADLINK_S1C_SENSOR_UPDATE"
EVENT_PROPERTY_NAME = "name"
EVENT_PROPERTY_STATE = "state"

SENSOR_TYPE_DOOR_SENSOR = "Door Sensor"
SENSOR_TYPE_DOOR_SENSOR_ICON = "mdi:door"
SENSOR_TYPE_MOTION_SENSOR = "Motion Sensor"
SENSOR_TYPE_MOTION_SENSOR_ICON = "mdi:walk"
SENSOR_TYPE_KEY_FOB = "Key Fob"
SENSOR_TYPE_KEY_FOB_ICON = "mdi:remote"
SENSOR_DEFAULT_ICON = "mdi:security-home"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    }
)


@asyncio.coroutine
def async_setup_platform(
    hass: HomeAssistant,
    config: Dict,
    async_add_devices: Callable,
    discovery_info: Optional[Dict] = None,
) -> bool:
    """Implementation for setting up the integration and create the sensor."""
    ip_address = config[CONF_IP_ADDRESS]
    mac = config[CONF_MAC].encode().replace(b":", b"")
    mac_addr = binascii.unhexlify(mac)
    timeout = config[CONF_TIMEOUT]

    conn_obj = HubConnection(ip_address, mac_addr, timeout)

    raw_data = conn_obj.get_initial_data()
    sensors = []
    for i, sensor in enumerate(raw_data["sensors"]):
        sensors.append(
            S1C_SENSOR(
                hass,
                sensor["name"],
                sensor["type"],
                conn_obj.parse_status(sensor["type"], str(sensor["status"])),
                now(),
            )
        )
    if sensors:
        async_add_devices(sensors, True)

    WatchSensors(hass, conn_obj).start()

    return True  # type: ignore


class S1C_SENSOR(Entity):
    """Representation of Home Assistant's sensor entity.

    Args:
      hass: Home Assistant instance.
      city: The city name to monitor.
      name: The sensor entity name.
      havdalah: Minutes for havdalah calculation after sundown.
      candle_light: Minutes for candle lighting calculation before sunset.

    """

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        sensor_type: str,
        status: str,
        last_changed: datetime.datetime,
    ) -> None:
        """Initialize the object."""
        self.entity_id = ENTITY_ID_FORMAT.format(
            name.replace(" ", "_").replace("-", "_").lower()
        )
        self._hass = hass
        self._name = name
        self._sensor_type = sensor_type
        self._state = status
        self._last_changed = last_changed

        hass.bus.async_listen(UPDATE_EVENT, self.async_event_listener)

    @property
    def name(self) -> str:
        """str: Return the name of the entity."""
        return self._name

    @property
    def should_poll(self) -> bool:
        """bool: Return false if entity pushes its state to HA."""
        return False

    @property
    def state(self) -> str:
        """str: Return the state of the entity."""
        return self._state

    @property
    def icon(self) -> str:
        """str: Return the icon to use in the frontend."""
        if self._sensor_type == SENSOR_TYPE_DOOR_SENSOR:
            return SENSOR_TYPE_DOOR_SENSOR_ICON
        elif self._sensor_type == SENSOR_TYPE_KEY_FOB:
            return SENSOR_TYPE_KEY_FOB_ICON
        elif self._sensor_type == SENSOR_TYPE_MOTION_SENSOR:
            return SENSOR_TYPE_MOTION_SENSOR_ICON
        else:
            return SENSOR_DEFAULT_ICON

    @property
    def device_state_attributes(self) -> Dict:
        """dict: Return device specific state attributes."""
        return {
            "sensor_type": self._sensor_type,
            "last_changed": self._last_changed,
        }

    @asyncio.coroutine
    def async_event_listener(self, event: Event) -> Generator:
        """Listen to events and update sensors state accordingly."""
        if event.data.get(EVENT_PROPERTY_NAME) == self._name:
            self._state = event.data.get(EVENT_PROPERTY_STATE)
            self._last_changed = event.time_fired
            yield from self.async_update_ha_state()


class HubConnection(object):
    """Representation of the Broadlink S1C Hub.

    Args:
      ip_addr: The static ip address of the hub.
      mac_addr: The mac address of the hub.
      timeout: The timout to consider connection lost.

    """

    def __init__(self, ip_addr: str, mac_addr: bytes, timeout: int) -> None:
        """Initialize the connection object."""
        import broadlink

        self._hub = broadlink.S1C((ip_addr, 80), mac_addr, None)
        self._hub.timeout = timeout
        self._authorized = self.authorize()
        if self._authorized:
            _LOGGER.info("succesfully connected to s1c hub")
            self._initial_data = self._hub.get_sensors_status()
        else:
            _LOGGER.error(
                "failed to connect s1c hub, not authorized."
                "Fix the problem and restart the system."
            )
            self._initial_data = None

    def authorize(self, retry: int = 3) -> bool:
        """Use for authorization for the hub connection.

        Args:
          retry: Number of times to retry on connection lost.

        """
        try:
            auth = self._hub.auth()
        except socket.timeout:
            auth = False
        if not auth and retry > 0:
            return self.authorize(retry - 1)
        return auth

    def get_initial_data(self) -> Dict:
        """dict: Return initial data for discovery."""
        return self._initial_data

    def get_hub_connection(self) -> S1C:
        """S1C: Return the connection object."""
        return self._hub

    def parse_status(self, sensor_type: str, sensor_status: str) -> str:
        """Use as parser for returning more human readable sensor state.

        Args:
          sensor_type: acceptable values:
            - Door Sensor
            - Motion Sensor
            - Key Fob
          sensor_status: hex status of the sensor: 0, 16, 32, 48, 64, 128, 144

        """
        if sensor_type == SENSOR_TYPE_DOOR_SENSOR and sensor_status in (
            "0",
            "128",
        ):
            return STATE_CLOSED
        elif sensor_type == SENSOR_TYPE_DOOR_SENSOR and sensor_status in (
            "16",
            "144",
        ):
            return STATE_OPEN
        elif sensor_type == SENSOR_TYPE_DOOR_SENSOR and sensor_status == "48":
            return STATE_TAMPERED
        elif sensor_type == SENSOR_TYPE_MOTION_SENSOR and sensor_status in (
            "0",
            "128",
        ):
            return STATE_NO_MOTION
        elif (
            sensor_type == SENSOR_TYPE_MOTION_SENSOR and sensor_status == "16"
        ):
            return STATE_MOTION_DETECTED
        elif (
            sensor_type == SENSOR_TYPE_MOTION_SENSOR and sensor_status == "32"
        ):
            return STATE_TAMPERED
        elif sensor_type == SENSOR_TYPE_KEY_FOB and sensor_status == "16":
            return STATE_ALARM_DISARMED
        elif sensor_type == SENSOR_TYPE_KEY_FOB and sensor_status == "32":
            return STATE_ALARM_ARMED_AWAY
        elif sensor_type == SENSOR_TYPE_KEY_FOB and sensor_status == "64":
            return STATE_ALARM_ARMED_HOME
        elif sensor_type == SENSOR_TYPE_KEY_FOB and sensor_status in (
            "0",
            "128",
        ):
            return STATE_ALARM_SOS
        else:
            _LOGGER.warning(
                "Unknown status %s for type %s.", sensor_status, sensor_type
            )
            return STATE_UNKNOWN


class WatchSensors(threading.Thread):
    """Representation of the object watching over sensor state changes."""

    def __init__(self, hass: HomeAssistant, conn_obj: S1C) -> None:
        """Initialize the watcher object and create the thread."""
        threading.Thread.__init__(self)
        self._hass = hass
        self._ok_to_run = False
        self._conn_obj = conn_obj
        self._last_exception_dt = None
        self._exception_count = 0
        if self._conn_obj._authorized:
            self._ok_to_run = True
            self._hub = self._conn_obj.get_hub_connection()

    def run(self) -> None:
        """Use for running the thread."""
        self._hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)

        if not (self._conn_obj.get_initial_data() is None):
            old_status = self._conn_obj.get_initial_data()
        else:
            old_status = self._hub.get_sensors_status()

        while self._ok_to_run:
            try:
                current_status = self._hub.get_sensors_status()
                for i, sensor in enumerate(current_status["sensors"]):
                    current_fixed_status = self._conn_obj.parse_status(
                        sensor["type"], str(sensor["status"])
                    )
                    previous_fixed_status = self._conn_obj.parse_status(
                        old_status["sensors"][i]["type"],
                        str(old_status["sensors"][i]["status"]),
                    )
                    if not (current_fixed_status == previous_fixed_status):
                        self.launch_state_change_event(
                            sensor["name"], current_fixed_status
                        )
                        old_status = current_status
            except:  # noqa: E722
                _LOGGER.warning(
                    "Exception while getting sensors status: %s",
                    traceback.format_exc(),
                )
                self.check_loop_run()
                continue

    def check_loop_run(self) -> None:
        """Check if it's ok to run the loop (no too many exceptions)."""
        max_exceptions_before_stop = 50
        max_minutes_from_last_exception = 1

        current_dt = now()
        if self._last_exception_dt is not None:
            if (
                self._last_exception_dt.year == current_dt.year
                and self._last_exception_dt.month == current_dt.month
                and self._last_exception_dt.day == current_dt.day
            ):
                calc_dt = current_dt - self._last_exception_dt
                diff = divmod(calc_dt.days * 86400 + calc_dt.seconds, 60)
                if diff[0] > max_minutes_from_last_exception:
                    self._exception_count = 0
                else:
                    self._exception_count += 1
            else:
                self._exception_count = 0
        else:
            self._exception_count = 0

        if max_exceptions_before_stop <= self._exception_count:
            _LOGGER.error(
                "Max exceptions allowed in watch loop exceeded."
                "Stoping watch loop"
            )
            self._ok_to_run = False

        self._last_exception_dt = current_dt

    def stop(self, event: Event) -> None:
        """Use for stopping the watcher when Home Assistant stops."""
        self._ok_to_run = False

    def launch_state_change_event(self, name, status):
        """Use for launching an Event when a sensor state chagnes."""
        self._hass.bus.fire(
            UPDATE_EVENT,
            {EVENT_PROPERTY_NAME: name, EVENT_PROPERTY_STATE: status},
        )
