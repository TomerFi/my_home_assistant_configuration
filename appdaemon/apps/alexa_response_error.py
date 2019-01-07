import little_helpers

class GenericErrorResponse(object):
  # object representing the base generic error response, do not use directly!
  # use any of the subclassess TemperatureOutOfRangeErrorResponse, ThermostatIsOffErrorResponse, InvalidDirectiveErrorResponse,
  # InvalidValueErrorResponse, BridgeUnreachableErrorResponse, NoSuchEndpointErrorResponse, InternalErrorResponse
  def __init__(self, request_object, error_type, error_message, namespace='Alexa', **kwargs):
    self.response_header = {
      "namespace": namespace,
      "name": "ErrorResponse",
      "messageId": little_helpers.get_uuid_str(),
      "correlationToken": request_object.correlationToken,
      "payloadVersion": "3"
    }
    
    self.response_endpoint = {
      "endpointId": request_object.endpointId
    }
    
    self.response_payload = {
      "type": error_type,
      "message": error_message
    }
    
    if kwargs is not None:
      for key, value in kwargs.items():
        self.response_payload[str(key)] = value

  def create_response(self):
    return {
      "event": {
        "header": self.response_header,
        "endpoint": self.response_endpoint,
        "payload": self.response_payload
      }
    }


class TemperatureOutOfRangeErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the requested temperature is out of range
  def __init__(self, request_object, message, min_value, max_value, scale="CELSIUS"):
    kwargs = {
      "validRange": {
        "minimumValue": {
          "value": min_value,
          "scale": scale
        },
        "maximumValue": {
          "value": max_value,
          "scale": scale
        }
      }
    }
    super(TemperatureOutOfRangeErrorResponse, self).__init__(request_object, "TEMPERATURE_VALUE_OUT_OF_RANGE", message, "Alexa", **kwargs)


class ThermostatIsOffErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the requested thermostat is off and not responding
  def __init__(self, request_object, message):
    super(ThermostatIsOffErrorResponse, self).__init__(request_object, 'THERMOSTAT_IS_OFF', message, 'Alexa.ThermostatController')


class InvalidDirectiveErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the request's directive is invalid
  def __init__(self, request_object, message):
    super(InvalidDirectiveErrorResponse, self).__init__(request_object, 'INVALID_DIRECTIVE', message)


class InvalidValueErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the requested value is not supported
  def __init__(self, request_object, message):
    super(InvalidValueErrorResponse, self).__init__(request_object, 'INVALID_VALUE', message)


class BridgeUnreachableErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the destination bridge is unreachable
  def __init__(self, request_object, message):
    super(BridgeUnreachableErrorResponse, self).__init__(request_object, 'BRIDGE_UNREACHABLE', message)


class NoSuchEndpointErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the requested endpoint doesn't exist
  def __init__(self, request_object, message):
    super(NoSuchEndpointErrorResponse, self).__init__(request_object, 'NO_SUCH_ENDPOINT', message)


class InternalErrorResponse(GenericErrorResponse):
  # object represnting the error response sent back when the requested endpoint doesn't exist
  def __init__(self, request_object, message):
    super(InternalErrorResponse, self).__init__(request_object, 'INTERNAL_ERROR', message)