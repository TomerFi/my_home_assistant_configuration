import appdaemon.plugins.hass.hassapi as hass
import little_helpers

class BatteryLowSendNotification(hass.Hass):
  """ ******************************************************************************************************************************
  *** Class for sending notification when the battery percent of the requested device has dropped below the configured threshold ***
  *******************************************************************************************************************************"""
  def initialize(self):
    # initialization of the class, register handler for event listening
    self.entity = self.args['sensor_entity']
    self.notify_service = self.args['notify_service'].replace('notify.', 'notify/')
    self.threshold_precent = int(self.args['threshold_precent'])
    self.device_name = self.args['device_name']
    self.state_handler = self.listen_state(self.battery_state_changed, self.entity)
    
  def battery_state_changed(self, entity, attribute, old, new, kwargs):
    # handles state change events and decides rarther the state qualifies for a notification send
    if int(new) <= self.threshold_precent and int(old) > self.threshold_precent:
      self.call_service(
        self.notify_service, title = "Battery Low",
        message = "Battery percent on " + self.device_name + "has dropped below the " + str(self.threshold_precent) + " threshold, please charge the device"
      )
  

class SensorsControlSwitches(hass.Hass):
  """ ********************************************************************************************************************
  *** Class for turning switch or switches on or off depending on the configured sensor states (off to on / on to off) ***
  *********************************************************************************************************************"""
  def initialize(self):
    # initialization of the class, register handler for event listening
    self.sensor_entity = self.args['sensor_entity']
    self.switch_entities = []
    if isinstance(self.args['switch_entities'], str):
      self.switch_entities.append(self.args['switch_entities'])
    else:
      for switch in self.args['switch_entities']:
        self.switch_entities.append(switch)
    self.turn_on_closed_to_open = self.args['turn_on_closed_to_open']
    self.turn_off_open_to_closed = self.args['turn_off_open_to_closed']
    self.state_handler = self.listen_state(self.state_changes, self.sensor_entity)
    
  def state_changes(self, entity, attribute, old, new, kwargs):
    # handles state change events and turning off the switch is the sensor changed from off to on and vice versa
    if self.turn_on_closed_to_open and str(old) in little_helpers.false_strings and str(new) in little_helpers.true_strings:
      for switch in self.switch_entities:
        self.call_service('switch/turn_on', entity_id = switch)
    elif self.turn_off_open_to_closed and str(old) in little_helpers.true_strings and str(new) in little_helpers.false_strings:
      for switch in self.switch_entities:
        self.call_service('switch/turn_off', entity_id = switch)

    
class CallServiceOnMqttMessage(hass.Hass):
  """ ******************************************************************
  *** Class for calling a service and pass data when on mqtt message ***
  *******************************************************************"""
  def initialize(self):
    # initialization of the class, register handler for event listening
    self.service = self.args['service'].replace('.', '/')
    self.data = self.args['data']
    
    self.message_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], payload = self.args['payload'], namespace = 'mqtt')
    
  def message_arrived(self, event_name, data, kwargs):
    # mqtt message handler, calls the service while passing the data
    self.call_service(self.service, **self.data)
    

class CallServiceOnStateChange(hass.Hass):
  """ ******************************************************************
  *** Class for calling a service and pass data when on state change ***
  *******************************************************************"""
  def initialize(self):
    # initialization of the class, register handler for event listening
    self.entity = self.args['entity']
    self.service = self.args['service'].replace('.', '/')
    self.service_data = self.args['service_data']
    
    if self.args['event_data']:
      self.state_handler = self.listen_state(self.state_changes, self.entity, **self.args['event_data'])
    else:
      self.state_handler = self.listen_state(self.state_changes, self.entity)

  def state_changes(self, entity, attribute, old, new, kwargs):
    # state change handler, calls the service while passing the data
    self.call_service(self.service, **self.service_data)
