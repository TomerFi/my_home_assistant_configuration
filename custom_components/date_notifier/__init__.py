"""Home Assistant Custom Component, Date Notifier and countdown.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

Example:
  .. code-block:: yaml

        date_notifier:
          # One Time Reminder will be send 1 day before the event date,
          # on date 2017-11-19 at 21:25
          one_time_reminder1:
            name: "one-time test"
            hour: 21
            minute: 25
            day: 20
            month: 11
            year: 2017
            message: "one-time test"
            days_notice: 1
            notifier: "notify_service_name"
            countdown: true
          # Yearly Reminder will be sent 2 days before the event every year,
          # on November 19th at 21:26
          yearly_reminder1:
            name: "yearly test"
            hour: 21
            minute: 26
            day: 21
            month: 11
            message: "yearly test"
            days_notice: 2
            notifier: "notify_service_name"
            countdown: false
          # Monthly Reminder will be send on the 19th of every month at 21:27
          monthly_reminder1:
            name: "montly test"
            hour: 21
            minute: 27
            day: 19
            message: "montly test2"
            notifier: "notify_service_name"
            countdown: true
          # Daily Reminder will be send every day at 21:28
          daily_reminder1:
            name: "daily test"
            hour: 21
            minute: 28
            message: "daily test"
            notifier: "notify_service_name"
            countdown: false

"""
import asyncio
import datetime
import logging
from typing import Dict, Generator, List, Optional, Tuple

import voluptuous as vol
from homeassistant.components.notify import DOMAIN as NOTIFY_DOMAIN
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [NOTIFY_DOMAIN]

DOMAIN = "date_notifier"
ENTITY_ID_FORMAT = DOMAIN + ".{}"

NAME = "name"
HOUR = "hour"
MINUTE = "minute"
MINUTE_DEFAULT = 0
DAY = "day"
MONTH = "month"
YEAR = "year"
MESSAGE = "message"
DAYS_NOTICE = "days_notice"
DAYS_NOTICE_DEFAULT = 0
NOTIFIER = "notifier"
COUNTDOWN = "countdown"
COUNTDOWN_DEFAULT = False

ATTR_PAST_DUE = "past_due"
ATTR_DAILY = "daily"
ATTR_MONTHLY = "monthly"
ATTR_YEARLY = "yearly"
ATTR_ON_DATE = "on_date"

RECURRENCE = "recurrence"
INTERVAL = datetime.timedelta(minutes=1)
SERVICE_SCAN_DATES = "scan_dates"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                cv.slug: vol.All(
                    {
                        vol.Required(NAME): cv.string,
                        vol.Required(HOUR): cv.positive_int,
                        vol.Required(MESSAGE): cv.string,
                        vol.Required(NOTIFIER): cv.string,
                        vol.Optional(
                            DAYS_NOTICE, default=DAYS_NOTICE_DEFAULT
                        ): cv.positive_int,
                        vol.Optional(DAY): cv.positive_int,
                        vol.Optional(
                            MINUTE, default=MINUTE_DEFAULT
                        ): cv.positive_int,
                        vol.Optional(MONTH): cv.positive_int,
                        vol.Optional(YEAR): cv.positive_int,
                        vol.Optional(
                            COUNTDOWN, default=COUNTDOWN_DEFAULT
                        ): cv.boolean,
                    }
                )
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


@asyncio.coroutine
def async_setup(hass: HomeAssistant, config: Dict) -> Generator:
    """Implementation for setting up the component."""
    component = EntityComponent(_LOGGER, DOMAIN, hass)
    entities = []
    for slug, config in config[DOMAIN].items():
        if not config:
            config = {}

        name = config[NAME]
        hour = config[HOUR]
        minute = config[MINUTE]
        day = None  # type: Optional[int]
        month = None  # type: Optional[int]
        year = None  # type: Optional[int]
        message = config[MESSAGE]
        days_notice = config[DAYS_NOTICE]
        notifier = config[NOTIFIER].replace(NOTIFY_DOMAIN + ".", "")
        countdown = config[COUNTDOWN]
        recurrence = ATTR_DAILY
        if config.get(DAY):
            day = config.get(DAY)
            recurrence = ATTR_MONTHLY
        if config.get(MONTH):
            month = config.get(MONTH)
            recurrence = ATTR_YEARLY
        if config.get(YEAR):
            year = config.get(YEAR)
            calc_date = datetime.datetime.now().replace(
                second=0, microsecond=0
            )
            notify_date = "{}-{}-{} {}:{}".format(
                str(year), str(month), str(day), str(hour), str(minute)
            )
            reminder_set = datetime.datetime.strptime(
                notify_date, "%Y-%m-%d %H:%M"
            ) + datetime.timedelta(-days_notice)
            if calc_date > reminder_set:
                recurrence = ATTR_PAST_DUE
            else:
                recurrence = ATTR_ON_DATE

        entities.append(
            DateNotifier(
                hass,
                slug,
                name,
                hour,
                minute,
                day,
                month,
                year,
                message,
                days_notice,
                notifier,
                recurrence,
                countdown,
            )
        )

    @asyncio.coroutine
    def async_scan_dates_service(call: ServiceCall) -> Generator:
        """Implementation of Home Assistant service for updating entities."""
        for entity in component.entities:
            target_notifiers = [entity]
            tasks = [notifier.scan_dates() for notifier in target_notifiers]
            if tasks:
                yield from asyncio.wait(tasks, loop=hass.loop)
            else:
                _LOGGER.error("no tasks initialized")

    async_track_time_interval(hass, async_scan_dates_service, INTERVAL)

    yield from component.async_add_entities(entities)
    return True


class DateNotifier(Entity):
    """Representation of Home Assistant's sensor entity.

    Args:
      hass: Home Assistant instance.
      slug: Slug for constructing the entity id.
      name: Friendly name.
      hour: Hours to get notification in.
      minute: Minutes to get notification in.
      day: Month day to get notification in.
      month: Month to get notification in.
      year: Year to get notification in.
      message: Message for the notification.
      days_notice: Number of days to notify before occurence.
      notifier: Home Assistant notifier service to send notifiers to.
      recurrence: Type of the notifier
        (past_due, daily, monthly, yearly, on_date).
      countdown: True for daily notifications from 'days_notice' to occurence.

    """

    def __init__(
        self,
        hass: HomeAssistant,
        slug: str,
        name: str,
        hour: int,
        minute: int,
        day: Optional[int],
        month: Optional[int],
        year: Optional[int],
        message: str,
        days_notice: int,
        notifier: str,
        recurrence: str,
        countdown: bool,
    ) -> None:
        """Initialize the object."""
        self.hass = hass
        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT, slug, hass=hass
        )
        self._name = name
        self._hour = hour
        self._minute = minute
        self._day = day
        self._month = month
        self._message = message
        self._days_notice = days_notice
        self._notifier = notifier
        self._year = year
        self._recurrence = recurrence
        self._countdown = countdown
        self._dates_list = []  # type: List[Tuple[datetime.datetime, int]]
        if self._recurrence != ATTR_PAST_DUE:
            if self._countdown and self._days_notice > 0:
                for i in range(0, self._days_notice + 1):
                    self._dates_list.append(self.create_due_date(i))
            else:
                self._dates_list.append(
                    self.create_due_date(self._days_notice)
                )

    @property
    def should_poll(self) -> bool:
        """bool: Return false if entity pushes its state to HA."""
        return False

    @property
    def name(self) -> str:
        """str: Return the name of the entity."""
        return self._name

    @property
    def state(self):
        """str: Return the state of the entity."""
        return self._recurrence

    @property
    def state_attributes(self) -> Dict:
        """dict: Return the state attributes."""
        attribs = {
            HOUR: self._hour,
            MINUTE: self._minute,
            MESSAGE: self._message,
            NOTIFIER: self._notifier,
            RECURRENCE: self._recurrence,
            COUNTDOWN: self._countdown,
        }
        if self._recurrence == ATTR_MONTHLY:
            attribs[DAY] = self._day
            attribs[DAYS_NOTICE] = self._days_notice
        elif self._recurrence == ATTR_YEARLY:
            attribs[DAY] = self._day
            attribs[MONTH] = self._month
            attribs[DAYS_NOTICE] = self._days_notice
        elif self._recurrence == ATTR_ON_DATE:
            attribs[DAY] = self._day
            attribs[MONTH] = self._month
            attribs[YEAR] = self._year
            attribs[DAYS_NOTICE] = self._days_notice
        return attribs

    @callback
    def create_due_date(
        self, days_notice: int
    ) -> Tuple[datetime.datetime, int]:
        calc_date = datetime.datetime.now()
        _days_notice = days_notice
        if self._recurrence == ATTR_ON_DATE:
            notify_date = "{}-{}-{} {}:{}".format(
                str(self._year),
                str(self._month),
                str(self._day),
                str(self._hour),
                str(self._minute),
            )
            reminder_set = datetime.datetime.strptime(
                notify_date, "%Y-%m-%d %H:%M"
            ) + datetime.timedelta(-days_notice)
            if calc_date >= reminder_set:
                self._recurrence = ATTR_PAST_DUE
        elif self._recurrence == ATTR_YEARLY:
            notify_date = "{}-{}-{} {}:{}".format(
                str(calc_date.year),
                str(self._month),
                str(self._day),
                str(self._hour),
                str(self._minute),
            )
            reminder_set = datetime.datetime.strptime(
                notify_date, "%Y-%m-%d %H:%M"
            ) + datetime.timedelta(-days_notice)
        elif self._recurrence == ATTR_MONTHLY:
            notify_date = "{}-{}-{} {}:{}".format(
                str(calc_date.year),
                str(calc_date.month),
                str(self._day),
                str(self._hour),
                str(self._minute),
            )
            reminder_set = datetime.datetime.strptime(
                notify_date, "%Y-%m-%d %H:%M"
            ) + datetime.timedelta(-days_notice)
        elif self._recurrence == ATTR_DAILY:
            notify_date = "{}-{}-{} {}:{}".format(
                str(calc_date.year),
                str(calc_date.month),
                str(calc_date.day),
                str(self._hour),
                str(self._minute),
            )
            reminder_set = datetime.datetime.strptime(
                notify_date, "%Y-%m-%d %H:%M"
            )
            _days_notice = 0

        return (reminder_set, _days_notice)

    @callback
    def scan_dates(self) -> Generator:
        """Use as callback for updating the entity state."""
        calc_date = datetime.datetime.now().replace(second=0, microsecond=0)
        if self._recurrence != ATTR_PAST_DUE:
            for reminder_set, days_notice in self._dates_list:
                if (
                    self._recurrence == ATTR_ON_DATE
                    and calc_date >= reminder_set
                ):
                    self._recurrence = ATTR_PAST_DUE
                if calc_date == reminder_set:
                    message = self._message
                    if days_notice == 0:
                        message = "{} is due today.".format(message)
                    elif days_notice == 1:
                        message = "{} is due tommorow.".format(message)
                    else:
                        message = "{} is due in {} days.".format(
                            message, str(days_notice)
                        )
                    service_data = {
                        "title": "DateNotifier",
                        "message": message,
                    }
                    self.hass.async_add_job(
                        self.hass.services.async_call(
                            NOTIFY_DOMAIN,
                            self._notifier,
                            service_data=service_data,
                            blocking=False,
                        )
                    )
                    yield from self.async_update_ha_state()
                    break
