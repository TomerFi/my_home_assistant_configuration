import appdaemon.plugins.hass.hassapi as hass
import json

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