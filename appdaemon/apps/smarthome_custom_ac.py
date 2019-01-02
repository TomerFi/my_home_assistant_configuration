import appdaemon.plugins.hass.hassapi as hassapi
import alexa_request
import alexa_response_error
import alexa_response_success

class AlexaCustomAC(hassapi.Hass):
  
  def initialize(self):
    self.climate_entities = []
    
    if isinstance(self.args["climate_entities"], str):
      self.climate_entities.append(self.args["climate_entities"])
    else:
      for entity_id in self.args["climate_entities"]:
        self.climate_entities.append(entity_id)
    
    self.handler = self.register_endpoint(self.api_call, "AlexaCustomAC")
        
  def api_call(self, request):
    init_namespace = request['directive']['header']['namespace']
    init_name = request['directive']['header']['name']

    if init_namespace == 'Alexa':
      if init_name == 'ReportState':
        self.request_object = alexa_request.EndpointRequest(request, init_namespace, init_name)
        return alexa_response_success.StateReportResponse(self.request_object, self.get_state(self.request_object.endpointId, attribute='all')).create_response(), 200
      else:
        return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "name " + init_name + " is unknown for namespace " + init_namespace + "."), 200
    
    elif init_namespace == 'Alexa.Discovery':
      # do not use error responses for discovery requests, either return a success request with no endpoints data or do not return anything!
      if init_name == 'Discover':
        self.request_object = alexa_request.DiscoveryRequest(request, init_namespace, init_name)
        endpoints_list = [{'entity_id': entity_id, 'friendly_name': self.get_state(entity_id, attribute='friendly_name')} for entity_id in self.climate_entities ]
        return alexa_response_success.DiscoveryResponse(self.request_object, endpoints_list).create_response(), 200
      else:
        return None, 200

    elif init_namespace == 'Alexa.PowerController':
      if init_name == "TurnOn" or init_name == "TurnOff":
        self.request_object = alexa_request.PowerControlRequest(request, init_namespace, init_name)
        # TODO - add return statement here
      else:
        return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "name " + init_name + " is unknown for namespace " + init_namespace + "."), 200
    
    elif init_namespace == 'Alexa.ThermostatController':
      if init_name == "SetTargetTemperature":
        self.request_object = alexa_request.SetThermostatTemperatureRequest(request, init_namespace, init_name)
        # TODO - add return statement here
      elif init_name == "AdjustTargetTemperature":
        self.request_object = alexa_request.AdjustThermostatTemperatureRequest(request, init_namespace, init_name)
        # TODO - add return statement here
      elif init_name == "SetThermostatMode":
        self.request_object = alexa_request.SetThermostatModeRequest(request, init_namespace, init_name)
        # TODO - add return statement here
      else:
        return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "name " + init_name + " is unknown for namespace " + init_namespace + "."), 200
    
    else:
      return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "namespace " + init_namespace + " is unknown."), 200
    
    return alexa_response_error.InternalErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "no response found for namespace " + init_namespace + " and name " + init_name + "."), 200
    
  def terminate(self):
    self.unregister_endpoint(self.handler)
