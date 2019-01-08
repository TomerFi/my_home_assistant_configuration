import appdaemon.plugins.hass.hassapi as hassapi
import alexa_request
import alexa_response_error
import alexa_response_success
import little_helpers

class AlexaCustomAC(hassapi.Hass):
  
  def initialize(self):
    # initialization of the class: collect arguemnts and register api endpoint
    self.entities = self.args["entities"] # list of climate entities for alexa
    self.default_mode_for_on = self.args["default_mode_for_on"] # default mode for 'alexa, turn on X, can either be heat or cool
    self.scale = self.args["scale"] if "scale" in self.args else "CELSIUS" # temperature unit for discovery directive
    
    # register the api endpoint, the uri for this endpoint will be https://<your_ha_ip_or_name>/api/appdaemon/AlexaCustomAC
    # please note that as for appdaemon 3.0.2, legacy password is requierd, please add the parameter key 'api_password' with you configured password
    self.handler = self.register_endpoint(self.api_call, "AlexaCustomAC")
    
  def terminate(self):
    # termination of the class, unregister the endpoint handler.
    self.unregister_endpoint(self.handler)
        
  def api_call(self, request):
    # callback function for api requests
    init_namespace = request['directive']['header']['namespace']
    init_name = request['directive']['header']['name']

    try:
      ##################################
      ######## Alexa Directive #########
      ##################################
      if init_namespace == 'Alexa':
        try:
          
          #################
          ## ReportState ##
          #################
          if init_name == 'ReportState':
            request_object = alexa_request.EndpointRequest(request, init_namespace, init_name)
            return alexa_response_success.StateReportResponse(request_object, self.get_state(little_helpers.endpointId_to_entityId(request_object.endpointId), attribute='all'), self.scale).create_response(), 200
          
          ######################################
          ## Unknown name for namespace Alexa ##
          ######################################
          else:
            return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "name " + init_name + " is unknown for namespace " + init_namespace + ".").create_response(), 200
        
        except Exception as ex:
          raise Exception("ReportState directive failed") from ex
      
      ##############################################
      ######### Alexa.Discovery Directive ##########
      ##############################################
      elif init_namespace == 'Alexa.Discovery':
        try:
          
          ##############
          ## Discover ##
          ##############
          # do not use error responses for discovery requests, either return a success request with no endpoints data or do not return anything!
          if init_name == 'Discover':
            request_object = alexa_request.DiscoveryRequest(request, init_namespace, init_name)
            endpoints_list = [self.get_state(entity, attribute="all")for entity in self.entities]
            return alexa_response_success.DiscoveryResponse(request_object, endpoints_list).create_response(), 200
          
          ################################################
          ## Unknown name for namespace Alexa.Discovery ##
          ################################################
          else:
            return None, 200
        
        except Exception as ex:
          raise Exception("Discovery directive failed") from ex
  
      #################################################
      ######## Alexa.PowerController Directive ########
      #################################################
      elif init_namespace == 'Alexa.PowerController':
        try:

          #################
          ## Turn On/Off ##
          #################
          if init_name == "TurnOn" or init_name == "TurnOff":
            request_object = alexa_request.PowerControlRequest(request, init_namespace, init_name)
            entity_id = little_helpers.endpointId_to_entityId(request_object.endpointId)
            if entity_id in self.entities:
              self.call_service("climate/set_operation_mode", entity_id = entity_id, operation_mode = self.default_mode_for_on if init_name == "TurnOn" else "off")
              return alexa_response_success.PowerControlResponse(request_object, self.get_state(entity_id, attribute='all')).create_response(), 200
    
            else:
              return alexa_response_error.NoSuchEndpointErrorResponse(request_object, "unknown endpoint " + self.request_object.endpointId).create_response(), 200
          
          ######################################################
          ## Unknown name for namespace Alexa.PowerController ##
          ######################################################
          else:
            return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "name " + init_name + " is unknown for namespace " + init_namespace + ".").create_response(), 200
        
        except Exception as ex:
          raise Exception("PowerControl directive failed") from ex
  
      ##############################################
      #### Alexa.ThermostatController Directive ####
      ##############################################
      elif init_namespace == 'Alexa.ThermostatController':
        try:
          
          #####################
          ## Set Temperature ##
          #####################
          if init_name == "SetTargetTemperature":
            request_object = alexa_request.SetThermostatTemperatureRequest(request, init_namespace, init_name)
            entity = self.get_state(little_helpers.endpointId_to_entityId(request_object.endpointId), attribute='all')
            
            if entity["state"].lower() == "off":
              return alexa_response_error.ThermostatIsOffErrorResponse(request_object, "endpoint is off").create_response(), 200
            
            targetTemp = float(round(request_object.value, 1))
    
            if targetTemp < entity["attributes"]["min_temp"] or targetTemp > entity["attributes"]["max_temp"]:
              return alexa_response_error.TemperatureOutOfRangeErrorResponse(request_object, "out of range", str(entity["attributes"]["min_temp"]), str(entity["attributes"]["max_temp"]), self.scale).create_response(), 200
    
            service_name = "climate/set_temperature"
            kwargs = {"entity_id": entity["entity_id"], "temperature": targetTemp}
            
            entity["attributes"]["temperature"] = targetTemp # adjustment was needed because the data is being retrieved before the service call ended
    
          ########################
          ## Adjust Temperature ##
          ########################
          elif init_name == "AdjustTargetTemperature":
            request_object = alexa_request.AdjustThermostatTemperatureRequest(request, init_namespace, init_name)
            entity = self.get_state(little_helpers.endpointId_to_entityId(request_object.endpointId), attribute='all')
            
            if entity["state"].lower() == "off":
              return alexa_response_error.ThermostatIsOffErrorResponse(request_object, "endpoint is off").create_response(), 200
            
            targetTemp = entity["attributes"]["temperature"] + (float(round(request_object.value, 1)))
            
            if targetTemp < entity["attributes"]["min_temp"] or targetTemp > entity["attributes"]["max_temp"]:
              return alexa_response_error.TemperatureOutOfRangeErrorResponse(request_object, "out of range", str(entity["attributes"]["min_temp"]), str(entity["attributes"]["max_temp"]), self.scale).create_response(), 200
    
            service_name = "climate/set_temperature"
            kwargs = {"entity_id": entity["entity_id"], "temperature": targetTemp}
            
            entity["attributes"]["temperature"] = targetTemp # adjustment was needed because the data is being retrieved before the service call ended
          
          ##############
          ## Set Mode ##
          ##############
          elif init_name == "SetThermostatMode":
            request_object = alexa_request.SetThermostatModeRequest(request, init_namespace, init_name)
            entity = self.get_state(little_helpers.endpointId_to_entityId(request_object.endpointId), attribute='all')
    
            service_name = "climate/set_operation_mode"
            kwargs = {"entity_id": entity["entity_id"], "operation_mode": request_object.value.lower()}
            
            entity["state"] = request_object.value.lower() # adjustment was needed because the data is being retrieved before the service call ended
    
          ###########################################################
          ## Unknown name for namespace Alexa.ThermostatController ##
          ###########################################################
          else:
            return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "name " + init_name + " is unknown for namespace " + init_namespace + ".").create_response(), 200
            
          self.call_service(service_name, **kwargs)
          
          return alexa_response_success.ThermostatControlResponse(request_object, entity, self.scale).create_response(), 200
      
        except Exception as ex:
          raise Exception("ThermostatController directive failed") from ex
    
      ######################
      ## Unknown Namepace ##
      ######################
      else:
        return alexa_response_error.InvalidDirectiveErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), "namespace " + init_namespace + " is unknown.").create_response(), 200

    #################################
    ## Handle all inner-exceptions ##
    #################################
    except Exception as ex:
      return alexa_response_error.InternalErrorResponse(alexa_request.GenericRequest(request, init_namespace, init_name), ex.message).create_response(), 200
