from datetime import datetime
import uuid

class DiscoveryResponse(object):
  # object represnting the discovery response, for errors in discovery use the success response with no endpoints
  def __init__(self, request_object, entities):
    self.response_header = {
      'namespace': 'Alexa.Discovery',
      'name': 'Discover.Response',
      'messageId': str(uuid.uuid4()),
      'payloadVersion': request_object.payloadVersion
    }
  
    self.response_payload = {
      'endpoints': []
    }
    
    for entity in entities:
      self.response_payload['endpoints'].append({
          'endpointId': entity['entity_id'],
          'friendlyName': entity['friendly_name'],
          'description': 'AC Custom Thermostat by TomerFi',
          'manufacturerName': 'TomerFi',
          'displayCategories': ['THERMOSTAT'],
          'cookie': {
          },
          'capabilities': [
            {
              'type': 'AlexaInterface',
              'interface': '"Alexa.ThermostatController',
              'version': '3',
              'properties': {
                'supported': [
                  {
                    'name': 'targetSetpoint'
                  },
                  {
                    'name': 'thermostatMode'
                  }
                  ],
                  'proactivelyReported': True,
                  'retrievable': True
              }
            },
            {
              'type': 'AlexaInterface',
              'interface': 'Alexa.TemperatureSensor',
              'version': '3',
              'properties': {
                'supported': [
                  {
                    'name': 'temperature'
                  }
                  ],
                  'proactivelyReported': True,
                  'retrievable': True
              }
            },
            {
              'type': 'AlexaInterface',
              'interface': 'Alexa.PowerController',
              'version': '3',
              'properties': {
                'supported': [
                  {
                    'name': 'powerState'
                  }
                  ],
                  'proactivelyReported': True,
                  'retrievable': True
              }
            }
            ]
        })


  def create_response(self):
    return {
      'event': {
        'header': self.response_header,
        'payload': self.response_payload
      } 
    }


class StateReportResponse(object):
  
  def __init__(self, request_object, entity):
    datetime_iso = str(datetime.utcnow().replace(microsecond=0).isoformat())   
    
    self.response_header = {
      "namespace": "Alexa",
      "name": "StateReport",
      "payloadVersion": request_object.payloadVersion,
      "messageId": str(uuid.uuid4()),
      "correlationToken": request_object.correlationToken
    }
    
    self.response_endpoint = {
      "endpointId": entity["entity_id"]
    }
    
    self.response_context = {
      "properties": [
        {
          "namespace": "Alexa.ThermostatController",
          "name": "targetSetpoint",
          "value": {
            "value": entity["attributes"]["temperature"],
            "scale": "CELSIUS"
          },
          "timeOfSample": datetime_iso,
          "uncertaintyInMilliseconds": 100
        },
        {
          "namespace": "Alexa.ThermostatController",
          "name": "thermostatMode",
          "value": entity["attributes"]["operation_mode"] if entity["attributes"]["operation_mode"] != 'off' else 'heat',
          "timeOfSample": datetime_iso,
          "uncertaintyInMilliseconds": 100
        },
        {
          "namespace": "Alexa.TemperatureSensor",
          "name": "temperature",
          "value": entity["attributes"]["current_temperature"],
          "timeOfSample":datetime_iso,
          "uncertaintyInMilliseconds": 100
        },
        {
          "namespace": "Alexa.PowerController",
          "name": "powerState",
          "value": 'off' if entity["attributes"]["operation_mode"] == 'off' else 'on',
          "timeOfSample": datetime_iso,
          "uncertaintyInMilliseconds": 100
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