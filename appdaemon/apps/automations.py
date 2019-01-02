import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.hass.hassplugin as plugin
import json
import global_data
import ir_packets

class WallPanelsExtractAttributesFromMessage(hass.Hass):
  """ ***********************************************************************************************************
  *** Class for extracting data from the wall panel app mqtt messages and save them as state attributes in HA ***
  ************************************************************************************************************"""
  def initialize(self):
    # initialization of the class, determine method to handle mqtt message
    self.entity = self.args['sensor_entity']
    if self.args['sensor_type'] == 'battery':
      self.battery_handler = self.listen_event(self.mqtt_battery_message, 'MQTT_MESSAGE', topic = self.args['sensor_topic'], namespace = 'mqtt')
    elif self.args['sensor_type'] == 'state':
      self.state_handler = self.listen_event(self.mqtt_state_message, 'MQTT_MESSAGE', topic = self.args['sensor_topic'], namespace = 'mqtt')

  def mqtt_battery_message(self, event_name, data, kwargs):
    # handle battery messages ie: {"value":47,"unit":"%","charging":false,"acPlugged":false,"usbPlugged":false}
    payload_data = json.loads(data['payload'])
       
    entity_state = payload_data['value']
    entity_attributes = self.get_state(self.entity, attribute='all')['attributes']
       
    entity_attributes['charging'] = payload_data['charging']
    entity_attributes['acPlugged'] = payload_data['acPlugged']
    entity_attributes['usbPlugged'] = payload_data['usbPlugged']

    self.set_state(self.entity, state = entity_state, attributes = entity_attributes)
    
  def mqtt_state_message(self, event_name, data, kwargs):
    # handle state messages ie: {"currentUrl":"http://hasbian:8123/states", "screenOn":true}
    payload_data = json.loads(data['payload'])
       
    entity_state = payload_data['screenOn']
    entity_attributes = self.get_state(self.entity, attribute='all')['attributes']
       
    entity_attributes['currentUrl'] = payload_data['currentUrl']

    self.set_state(self.entity, state = entity_state, attributes = entity_attributes)


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
    if self.turn_on_closed_to_open and str(old) in global_data.false_strings and str(new) in global_data.true_strings:
      for switch in self.switch_entities:
        self.call_service('switch/turn_on', entity_id = switch)
    elif self.turn_off_open_to_closed and str(old) in global_data.true_strings and str(new) in global_data.false_strings:
      for switch in self.switch_entities:
        self.call_service('switch/turn_off', entity_id = switch)

        
class CeilingFanMqttMessageToIRPacket(hass.Hass):
  """ ********************************************************************************************************************************
  *** Class sending ceiling fan ir packets to with the confifured command to the specific service from the configured room blaster ***
  *********************************************************************************************************************************"""
  def initialize(self):
    # initialization of the class, register handler for event listening
    self.room = self.args['room']
    self.command = self.args['command']
    if self.args['payload']:
      self.fan_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], payload = self.args['payload'], namespace = 'mqtt')
    else:
      self.fan_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], namespace = 'mqtt')

  def message_arrived(self, event_name, data, kwargs):
    # mqtt message handler, gets the service and packet based on the room and command
    service_name, ir_packet = ir_packets.get_fan_service_and_packet(self.room, self.command)
    self.call_service(service_name, packet = ir_packet)


class ACMqttMessageToIRPacket(hass.Hass):
  
  def initialize(self):
    self.room = self.args['room']
    self.mode = self.args['mode']
    self.speed = self.args['speed'] if self.args['speed'] else None
    self.temp = self.args['temp'] if self.args['temp'] else None
    
    if self.args['payload']:
      self.ac_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], payload = self.args['payload'], namespace = 'mqtt')
    else:
      self.ac_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], namespace = 'mqtt')
    
  def message_arrived(self, event_name, data, kwargs):
    # mqtt message handler, gets the service and packet based on the room and command details
    service_name, ir_packet = ir_packets.get_ac_service_and_packet(self.room, self.command, self.speed, self.temp)
    self.call_service(service_name, packet = ir_packet)

    
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
    

class HandleMqttACUnit(hass.Hass):
  
  def initialize(self):
    #self.room = self.args['room']
    #self.climate_entity = self.args['climate_entity']
    #self.sensor_entity = self.args['sensor_entity']
    #self.mode_select = self.args['mode_select']
    #self.fan_select = self.args['fan_select']
    #self.temperature_number = self.args['temperature_number']
    
    config = self.get_hass_config
    self.log('test')
    
