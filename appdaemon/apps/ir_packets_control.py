import appdaemon.plugins.hass.hassapi as hass
import little_helpers
import ir_packets_manager

class HandleMqttFan(hass.Hass):
  def initialize(self):
    # initialization of the class, register handler for event listening
    self.ir_send_service = little_helpers.fix_service_domain(self.args["ir_send_service"])
    self.fan_type = self.args["fan_type"]
    self.command = self.args['command']
    
    if self.args['payload']:
      self.fan_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], payload = self.args['payload'], namespace = 'mqtt')
    else:
      self.fan_handler = self.listen_event(self.message_arrived, 'MQTT_MESSAGE', topic = self.args['topic'], namespace = 'mqtt')

  def terminate(self):
    self.cancel_listen_event(self.fan_handler)

  def message_arrived(self, event_name, data, kwargs):
    # mqtt message handler, gets the service and packet based on the room and command
    self.call_service(self.ir_send_service, packet = ir_packets_manager.get_fan_packet(self.fan_type, self.command))


class HandleMqttACUnit(hass.Hass):
  def initialize(self):
    self.climate_entity = self.args["climate_entity"]
    self.default_mode_for_on = self.args["default_mode_for_on"]
    self.ir_send_service = little_helpers.fix_service_domain(self.args["ir_send_service"])
    self.ac_type = self.args["ac_type"]
    self.mode_command_topic = self.args["mode_command_topic"]
    self.mode_entity_for_update = self.args["mode_entity_for_update"] if self.args["mode_entity_for_update"] else None
    self.temperature_command_topic = self.args["temperature_command_topic"]
    self.temperature_entity_for_update = self.args["temperature_entity_for_update"] if self.args["temperature_entity_for_update"] else None
    self.fan_mode_command_topic = self.args["fan_mode_command_topic"]
    self.fan_mode_entity_for_update = self.args["fan_mode_entity_for_update"] if self.args["fan_mode_entity_for_update"] else None
    
    self.mode_command_handler = self.listen_event(self.on_mode_command, 'MQTT_MESSAGE', topic = self.mode_command_topic, namespace = 'mqtt')
    self.temperature_command_handler = self.listen_event(self.on_temperature_command, 'MQTT_MESSAGE', topic = self.temperature_command_topic, namespace = 'mqtt')
    self.fan_mode_command_handler = self.listen_event(self.on_fan_mode_command, 'MQTT_MESSAGE', topic = self.fan_mode_command_topic, namespace = 'mqtt')
    
  def terminate(self):
    self.cancel_listen_event(self.mode_command_handler)
    self.cancel_listen_event(self.temperature_command_handler)
    self.cancel_listen_event(self.fan_mode_command_handler)

  def on_mode_command(self, event_name, data, kwargs):
    if data["payload"] in little_helpers.false_strings:
      packet = ir_packets_manager.get_ac_packet(self.ac_type, data["payload"])

    else:
      entity_data = self.get_state(self.climate_entity, attribute="all")
      packet = ir_packets_manager.get_ac_packet(self.ac_type, data["payload"], entity_data["attributes"]["fan_mode"], entity_data["attributes"]["temperature"])

    self.send_packet(packet)
    if (self.mode_entity_for_update):
      self.update_internal_ha_state(self.mode_entity_for_update, data["payload"].lower())

  def on_temperature_command(self, event_name, data, kwargs):
    entity_data = self.get_state(self.climate_entity, attribute="all")
    self.send_packet(ir_packets_manager.get_ac_packet(self.ac_type, entity_data["state"], entity_data["attributes"]["fan_mode"], float(data["payload"])))
    if (self.temperature_entity_for_update):
        self.update_internal_ha_state(self.temperature_entity_for_update, float(data["payload"]))
  
  def on_fan_mode_command(self, event_name, data, kwargs):
    entity_data = self.get_state(self.climate_entity, attribute="all")
    self.send_packet(ir_packets_manager.get_ac_packet(self.ac_type, entity_data["state"], data["payload"], entity_data["attributes"]["temperature"]))
    if (self.fan_mode_entity_for_update):
        self.update_internal_ha_state(self.fan_mode_entity_for_update, data["payload"])

  def send_packet(self, packet):
    self.call_service(self.ir_send_service, packet = packet)
    
  def update_internal_ha_state(self, entity_id, to_state):
    entity = self.get_state(entity_id, attribute="all")
    if entity["state"] != to_state:
      self.set_state(entity_id, state = to_state, attributes = entity["attributes"])
    
    
class TemperatureSensorToMqtt(hass.Hass):
  def initialize(self):
    self.sensor_entity = self.args["sensor_entity"]
    self.topic = self.args["topic"]
    
    self.state_handler = self.listen_state(self.state_changed, entity = self.sensor_entity)
    
  def terminate(self):
    self.cancel_listen_state(self.state_handler)
    
  def state_changed(self, entity, attribute, old, new, kwargs):
    self.call_service("mqtt/publish", **{"topic": self.topic, "payload": new })
