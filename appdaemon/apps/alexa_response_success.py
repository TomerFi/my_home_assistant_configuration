import little_helpers

class DiscoveryResponse(object):
  # object represnting the discovery response, for errors in discovery use the success response with no endpoints
  def __init__(self, request_object, entities):
    self.response_header = {
      "namespace": "Alexa.Discovery",
      "name": "Discover.Response",
      "messageId": little_helpers.get_uuid_str(),
      "payloadVersion": "3"
    }
  
    self.response_payload = {
      "endpoints": []
    }

    for entity in entities:
      supported_modes = []
      for mode in entity['attributes']['operation_list']:
        supported_modes.append(mode.upper())
      
      self.response_payload["endpoints"].append({
          "endpointId": little_helpers.entityId_to_endpointId(entity["entity_id"]),
          "friendlyName": entity['attributes']["friendly_name"],
          "description": "AC Custom Thermostat by TomerFi",
          "manufacturerName": "TomerFi",
          "displayCategories": ["THERMOSTAT", "TEMPERATURE_SENSOR"],
          "cookie": {
          },
          "capabilities": [
            {
              "type": "AlexaInterface",
              "interface": "Alexa.ThermostatController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "targetSetpoint"
                  },
                  {
                    "name": "thermostatMode"
                  }
                  ],
                  "proactivelyReported": True,
                  "retrievable": True
              },
              "configuration": {
                "supportsScheduling": False,
                "supportedModes": supported_modes
              }
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.TemperatureSensor",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "temperature"
                  }
                  ],
                  "proactivelyReported": True,
                  "retrievable": True
              }
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.PowerController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "powerState"
                  }
                  ],
                  "proactivelyReported": True,
                  "retrievable": True
              }
            }
            ]
        })

  def create_response(self):
    return {
      "event": {
        "header": self.response_header,
        "payload": self.response_payload
      }
    }


class StateReportResponse(object):
  
  def __init__(self, request_object, entity, scale):
    datetime_iso = little_helpers.get_iso_datetime_utc_tz_str()
    uncertainty_milliseconds = little_helpers.get_elapsed_in_milliseconds(entity["last_updated"])

    self.response_header = {
      "namespace": "Alexa",
      "name": "StateReport",
      "payloadVersion": "3",
      "messageId": little_helpers.get_uuid_str(),
      "correlationToken": request_object.correlationToken
    }
    
    self.response_endpoint = {
      "endpointId": little_helpers.entityId_to_endpointId(entity["entity_id"])
    }
    
    self.response_context = {
      "properties": [
        {
          "namespace": "Alexa.ThermostatController",
          "name": "targetSetpoint",
          "value": {
            "value": entity["attributes"]["temperature"],
            "scale": scale
          },
          "timeOfSample": datetime_iso,
          "uncertaintyInMilliseconds": uncertainty_milliseconds
        },
        {
          "namespace": "Alexa.ThermostatController",
          "name": "thermostatMode",
          "value": entity["state"].upper(),
          "timeOfSample": datetime_iso,
          "uncertaintyInMilliseconds": uncertainty_milliseconds
        },
        {
          "namespace": "Alexa.TemperatureSensor",
          "name": "temperature",
          "value": {
            "value": entity["attributes"]["current_temperature"],
            "scale": scale
          },
          "timeOfSample":datetime_iso,
          "uncertaintyInMilliseconds": uncertainty_milliseconds
        },
        {
          "namespace": "Alexa.PowerController",
          "name": "powerState",
          "value": "OFF" if entity["state"].upper() == "OFF" else "ON",
          "timeOfSample": datetime_iso,
          "uncertaintyInMilliseconds": uncertainty_milliseconds
        }
        ]
    }
    
  def create_response(self):
    return {
      "context": self.response_context,
      "event": {
        "header": self.response_header,
        "endpoint": self.response_endpoint,
        "payload": {}
      }
    }
    

class PowerControlResponse(object):
  
  def __init__(self, request_object, entity):
    datetime_iso = little_helpers.get_iso_datetime_utc_tz_str()
    uncertainty_milliseconds = little_helpers.get_elapsed_in_milliseconds(entity["last_updated"])
    
    self.response_header = {
      "namespace": "Alexa",
      "name": "Response",
      "payloadVersion": "3",
      "messageId": little_helpers.get_uuid_str(),
      "correlationToken": request_object.correlationToken
    }
    
    self.response_endpoint = {
      "endpoint": {
        "scope": {
          "type": request_object.tokenType,
          "token": request_object.token
        },
        "endpointId": little_helpers.entityId_to_endpointId(entity["entity_id"])
      }
    }
    
    self.response_context = {
      "properties": [{
       "namespace": "Alexa.PowerController",
       "name": "powerState",
       "value": "OFF" if entity["state"].upper() == "OFF" else "ON",
       "timeOfSample": datetime_iso,
       "uncertaintyInMilliseconds": uncertainty_milliseconds
      }]
      
    }
    
  def create_response(self):
    return {
    "context": self.response_context,
    "event": {
      "header": self.response_header,
      "endpoint": self.response_endpoint,
      "payload": {}
    }
  }
  
class ThermostatControlResponse(object):
  
  def __init__(self, request_object, entity, scale):
    datetime_iso = little_helpers.get_iso_datetime_utc_tz_str()
    uncertainty_milliseconds = little_helpers.get_elapsed_in_milliseconds(entity["last_updated"])
    
    self.response_context = {
      "properties": [{
        "namespace": "Alexa.ThermostatController",
        "name": "targetSetpoint",
        "value": {
          "value": entity["attributes"]["temperature"],
          "scale": scale
        },
        "timeOfSample": datetime_iso,
        "uncertaintyInMilliseconds": uncertainty_milliseconds
      },
      {
        "namespace": "Alexa.ThermostatController",
        "name": "thermostatMode",
        "value": entity["state"].upper(),
        "timeOfSample": datetime_iso,
        "uncertaintyInMilliseconds": uncertainty_milliseconds
      }]
    }
    
    self.response_header = {
      "namespace": "Alexa",
      "name": "Response",
      "payloadVersion": "3",
      "messageId": little_helpers.get_uuid_str(),
      "correlationToken": request_object.correlationToken
    }
    
    self.response_endpoint = {
      "endpointId": little_helpers.entityId_to_endpointId(entity["entity_id"])
    }
  
  def create_response(self):
    return {
    "context": self.response_context,
    "event": {
      "header": self.response_header,
      "endpoint": self.response_endpoint,
      "payload": {}
    }
  }
  