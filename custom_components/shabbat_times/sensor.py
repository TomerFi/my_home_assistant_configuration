"""Home Assistant Custom Component, Shabbat Times sensor entity.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

Example:
  .. code-block:: yaml

        sensor:
          - platform: shabbat_times
            geonames: "IL-Haifa,IL-Rishon LeZion"
            havdalah_minutes_after_sundown: 42
            candle_lighting_minutes_before_sunset: 30

"""
import datetime
import json
import logging
from typing import Callable, Dict, Optional

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

GEONAMES = "geonames"
HAVDALAH_MINUTES = "havdalah_minutes_after_sundown"
CANDLE_LIGHT_MINUTES = "candle_lighting_minutes_before_sunset"

HAVDALAH_DEFAULT = 42
CANDLE_LIGHT_DEFAULT = 30
SCAN_INTERVAL = datetime.timedelta(seconds=60)

SHABBAT_START = "shabbat_start"
SHABBAT_END = "shabbat_end"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(GEONAMES): cv.string,
        vol.Optional(HAVDALAH_MINUTES, default=HAVDALAH_DEFAULT): int,
        vol.Optional(CANDLE_LIGHT_MINUTES, default=CANDLE_LIGHT_DEFAULT): int,
        vol.Optional(
            CONF_SCAN_INTERVAL, default=SCAN_INTERVAL
        ): cv.time_period,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: Dict,
    add_devices: Callable,
    discovery_info: Optional[Dict] = None,
) -> None:
    """Implementation for setting up the integration and create the sensor."""
    havdalah = config[HAVDALAH_MINUTES]
    candle_light = config[CANDLE_LIGHT_MINUTES]
    cities = config[GEONAMES]
    cities_list = cities.split(",")

    add_devices(
        [
            ShabbatTimes(
                hass,
                city,
                "Shabbat Times {}".format(city.replace("-", "_")),
                havdalah,
                candle_light,
            )
            for city in cities_list
        ]
    )


class ShabbatTimes(Entity):
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
        city: str,
        name: str,
        havdalah: int,
        candle_light: int,
    ) -> None:
        """Initialize the object."""
        self._hass = hass
        self._city = city
        self._name = name
        self._havdalah = havdalah
        self._candle_light = candle_light
        self._state = "Awaiting Update"
        self._shabbat_start = None  # type: Optional[datetime.datetime]
        self._shabbat_end = None  # type: Optional[datetime.datetime]

    @property
    def name(self) -> str:
        """str: Return the name of the entity."""
        return self._name

    @property
    def state(self) -> str:
        """str: Return the state of the entity."""
        return self._state

    @property
    def device_state_attributes(self) -> Dict:
        """dict: Return device specific state attributes."""
        return {
            SHABBAT_START: self._shabbat_start,
            SHABBAT_END: self._shabbat_end,
            HAVDALAH_MINUTES: self._havdalah,
            CANDLE_LIGHT_MINUTES: self._candle_light,
        }

    @Throttle(SCAN_INTERVAL)
    def update(self) -> None:
        """Implementation of the update method, used to update the state."""
        self._state = "Working"
        self.shabbat_start = None
        self._shabbat_end = None
        today = datetime.date.today()
        if today.weekday() == 5:
            friday = today + datetime.timedelta(-1)
        else:
            friday = today + datetime.timedelta((4 - today.weekday()) % 7)

        saturday = friday + datetime.timedelta(+1)

        year = str(friday.year)
        month = ("0" + str(friday.month))[-2:]

        hebcal_url = (
            "http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=off&min=off"
            "&mod=off&nx=off&year={}&month={}&ss=off&mf=off&c=on&geo=city"
            "&city={}&m={}&s=off&i=off&b={}"
        ).format(
            year,
            month,
            self._city,
            str(self._havdalah),
            str(self._candle_light),
        )

        hebcal_response = requests.get(hebcal_url)
        hebcal_json_input = hebcal_response.text
        hebcal_decoded = json.loads(hebcal_json_input)

        if "error" in hebcal_decoded:
            self._state = hebcal_decoded["error"]
            _LOGGER.error(hebcal_decoded["error"])
        else:
            for item in hebcal_decoded["items"]:
                if item["category"] == "candles":
                    ret_date = datetime.datetime.strptime(
                        item["date"][0:-6].replace("T", " "),
                        "%Y-%m-%d %H:%M:%S",
                    )
                    if ret_date.date() == friday:
                        self._shabbat_start = ret_date
                elif item["category"] == "havdalah":
                    ret_date = datetime.datetime.strptime(
                        item["date"][0:-6].replace("T", " "),
                        "%Y-%m-%d %H:%M:%S",
                    )
                    if ret_date.date() == saturday:
                        self._shabbat_end = ret_date

            self._state = "Updated"
