class GenericRequest(object):
  # object represnting the generic request, do not use directly (unless on errors)!
  # either use the EndpointRequest subclass for request invloving endpoint data or the DiscoveryRequest subclass for discovery requests
  # do not use error responses for discovery requests, either return a success request with no endpoints data or do not return anything!
  def __init__ (self, request, init_namespace, init_name):
    self._rawRequest = request
    self._namespace = init_namespace
    self._name = init_name
    self._payloadVersion = request['directive']['header']['payloadVersion']
    self._messageId = request['directive']['header']['messageId']

  @property
  def rawRequest(self):
    return self._rawRequest
  
  @property
  def namespace(self):
    return self._namespace
    
  @property
  def name(self):
    return self._name
  
  @property
  def payloadVersion(self):
    return self._payloadVersion
    
  @property
  def messageId(self):
    return self._messageId


class EndpointRequest(GenericRequest):
  # object represnting requests containing endpoint data, use directly for report state requests only!
  # for other types of requests use any of the subclassess AdjustThermostatTemperatureRequest, SetThermostatTemperatureRequest, SetThermostatModeRequest or PowerControlRequest
  def __init__(self, request, init_namespace, init_name):
    super(EndpointRequest, self).__init__(request, init_namespace, init_name)
    self._correlationToken = request['directive']['header']['correlationToken']
    self._endpointId = request['directive']['endpoint']['endpointId']
    self._tokenType = request['directive']['endpoint']['scope']['type']
    self._token = request['directive']['endpoint']['scope']['token']

  @property
  def correlationToken(self):
    return self._correlationToken
    
  @property
  def endpointId(self):
    return self._endpointId
  
  @property
  def tokenType(self):
    return self._tokenType
    
  @property
  def token(self):
    return self._token


class DiscoveryRequest(GenericRequest):
  # object represnting discovery requests
  def __init__(self, request, init_namespace, init_name):
    super(DiscoveryRequest, self).__init__(request, init_namespace, init_name)
    self._tokenlType = request['directive']['payload']['scope']['type']
    self._token = request['directive']['payload']['scope']['token']

  @property
  def tokenlType(self):
    return self._tokenlType
    
  @property
  def token(self):
    return self._token
    

class AdjustThermostatTemperatureRequest(EndpointRequest):
  # object represnting the adjust tempereture by delta request
  def __init__(self, request, init_namespace, init_name):
     super(AdjustThermostatTemperatureRequest, self).__init__(request, init_namespace, init_name)
     self._value = request['directive']['payload']['targetSetpointDelta']['value']
     self._scale = request['directive']['payload']['targetSetpointDelta']['scale']

  @property
  def value(self):
    return self._value
    
  @property
  def scale(self):
    return self._scale
    

class SetThermostatTemperatureRequest(EndpointRequest):
  # object represnting the set the tempereture to x request
  def __init__(self, request, init_namespace, init_name):
     super(SetThermostatTemperatureRequest, self).__init__(request, init_namespace, init_name)
     self._value = request['directive']['payload']['targetSetpoint']['value']
     self._scale = request['directive']['payload']['targetSetpoint']['scale']

  @property
  def value(self):
    return self._value
    
  @property
  def scale(self):
    return self._scale
    

class SetThermostatModeRequest(EndpointRequest):
  # object represnting the set the mode to to x request
  def __init__(self, request, init_namespace, init_name):
     super(SetThermostatModeRequest, self).__init__(request, init_namespace, init_name)
     self._value = request['directive']['payload']['thermostatMode']['value']

  @property
  def value(self):
    return self._value


class PowerControlRequest(EndpointRequest):
  # object represnting the set the mode to to x request
  def __init__(self, request, init_namespace, init_name):
     super(PowerControlRequest, self).__init__(request)
     self._powerState = True if self.name == 'TurnOn' else False

  @property
  def powerState(self):
    return self._powerState
    