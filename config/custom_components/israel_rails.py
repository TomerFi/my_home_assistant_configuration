import asyncio
import logging
import json
import datetime
import requests

import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.restore_state import async_get_last_state
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = []

DOMAIN = 'israel_rails'
ENTITY_ID_FORMAT = DOMAIN + '.{}'

NAME = 'name'
FROM_STATION = 'from_station'
TO_STATION = 'to_station'
DEPARTURE_TIME = 'departure_time'
FROM_PLATFORM = 'from_platform'
ESTIMATED_TIME = 'estimated_time'
ARRIVAL_TIME = 'arrival_time'
DEST_PLATFORM = 'dest_platform'
TRAIN_NUMBER = 'train_number'

INTERVAL = datetime.timedelta(minutes=5)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: vol.All({
            vol.Required(NAME): cv.string,
            vol.Required(FROM_STATION): vol.In(['1220', '1240', '1250', '1260', '1280', '1300', '1400', '1500', '1600',
                                                '1820', '1840', '2100', '2200', '2300', '2500', '2800', '2820', '300',
                                                '3100', '3300', '3310', '3400', '3500', '3600', '3700', '400', '4100',
                                                '4170', '4250', '4600', '4640', '4660', '4680', '4690', '4800', '4900',
                                                '5000', '5010', '5150', '5200', '5300', '5410', '5800', '5900', '6300',
                                                '6500', '6700', '700', '7000', '7300', '7320', '7500', '8550', '8600',
                                                '8700', '8800', '9000', '9100', '9200', '9600', '9650', '9700', '9800']),
            vol.Required(TO_STATION): vol.In(['1220', '1240', '1250', '1260', '1280', '1300', '1400', '1500', '1600',
                                              '1820', '1840', '2100', '2200', '2300', '2500', '2800', '2820', '300',
                                              '3100', '3300', '3310', '3400', '3500', '3600', '3700', '400', '4100',
                                              '4170', '4250', '4600', '4640', '4660', '4680', '4690', '4800', '4900',
                                              '5000', '5010', '5150', '5200', '5300', '5410', '5800', '5900', '6300',
                                              '6500', '6700', '700', '7000', '7300', '7320', '7500', '8550', '8600',
                                              '8700', '8800', '9000', '9100', '9200', '9600', '9650', '9700', '9800'])
        })
    })
}, extra=vol.ALLOW_EXTRA)


@asyncio.coroutine
def async_setup(hass, config):
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    entities = []

    for name, config in config[DOMAIN].items():
        if not config:
            config = {}

        name = config.get(NAME)
        from_station = config.get(FROM_STATION)
        to_station = config.get(TO_STATION)

        entities.append(IsraelRail(name, from_station, to_station))

    @asyncio.coroutine
    def async_update_rail_state_service(call):
        for entity_id in component.entities:
            entity = component.entities[entity_id]

            if entity:
                rails = [entity]
                tasks = [rail.async_update_rail_state() for rail in rails]
                if tasks:
                    yield from asyncio.wait(tasks, loop=hass.loop)
                else:
                    _LOGGER.error('no tasks initialized for ' + entity_id)
            else:
                _LOGGER.error('no entity found with the name ' + entity_id)

    async_track_time_interval(hass, async_update_rail_state_service, INTERVAL)

    yield from component.async_add_entities(entities)
    return True


class IsraelRail(Entity):

    def __init__(self, name, from_station, to_station):
        self.entity_id = ENTITY_ID_FORMAT.format((name.replace('-', '').replace(' ', '_')).lower())
        self._name = name
        self._from_station = from_station
        self._to_station = to_station
        self._departure_time = None
        self._from_platform = None
        self._estimated_time = None
        self._arrival_time = None
        self._dest_platform = None
        self._train_number = None
        self._update_status = 'waiting for update'

    @asyncio.coroutine
    def async_added_to_hass(self):
        state = yield from async_get_last_state(self.hass, self.entity_id)
        if state:
            self._value = state.state

    @property
    def state(self):
        return self._update_status

    @property
    def state_attributes(self):
        return{
            NAME: self._name,
            FROM_STATION: self._from_station,
            TO_STATION: self._to_station,
            DEPARTURE_TIME: self._departure_time,
            FROM_PLATFORM: self._from_platform,
            ESTIMATED_TIME: self._estimated_time,
            ARRIVAL_TIME: self._arrival_time,
            DEST_PLATFORM: self._dest_platform,
            TRAIN_NUMBER: self._train_number
        }

    @callback
    def async_update_rail_state(self):

        departure_time = None

        current_date = datetime.datetime.now().replace(second=0, microsecond=0)
        api_url = 'http://www.rail.co.il/apiinfo/api/Plan/GetRoutes?OId=' + self._from_station + '&TId=' + self._to_station + '&Date=' + str(current_date.year) + str(current_date.month) + str(current_date.day) + '&Hour=2200'
        api_response = requests.get(api_url)
        api_json_input = api_response.text
        api_decoded = json.loads(api_json_input)

        routes = api_decoded['Data']

        if routes:
            for route in routes['Routes']:
                train = route['Train'][0]
                if departure_time:
                    if datetime.datetime.strptime(train['DepartureTime'], '%d/%m/%Y %H:%M:%S') < datetime.datetime.strptime(departure_time, '%d/%m/%Y %H:%M:%S') and datetime.datetime.strptime(train['DepartureTime'], '%d/%m/%Y %H:%M:%S') > current_date:
                        departure_time = train['DepartureTime']
                        from_paltform = train['Platform']
                        estimated_time = route['EstTime']
                        arrival_time = train['ArrivalTime']
                        dest_platform = train['DestPlatform']
                        train_number = train['Trainno']

                elif datetime.datetime.strptime(train['DepartureTime'], '%d/%m/%Y %H:%M:%S') > current_date:
                    departure_time = train['DepartureTime']
                    from_paltform = train['Platform']
                    estimated_time = route['EstTime']
                    arrival_time = train['ArrivalTime']
                    dest_platform = train['DestPlatform']
                    train_number = train['Trainno']

        if departure_time:
            self._update_status = 'The next train is in ' + departure_time.split(' ')[1]
            self._departure_time = departure_time
            self._from_platform = from_paltform
            self._estimated_time = estimated_time
            self._arrival_time = arrival_time
            self._dest_platform = dest_platform
            self._train_number = train_number
        else:
            self._update_status = 'No routes found for today'
            self._departure_time = None
            self._from_platform = None
            self._estimated_time = None
            self._arrival_time = None
            self._dest_platform = None
            self._train_number = None

        yield from self.async_update_ha_state()
