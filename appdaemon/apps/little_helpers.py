from datetime import datetime, timezone
import pytz
from uuid import uuid4

true_strings = ['True', 'true', 'Online', 'online', 'ON', 'On', 'on', 'Open', 'open', 'Motion Detected', 'motion_detected']
false_strings = ['False', 'false', 'Offline', 'offline', 'OFF', 'Off', 'off', 'Closed', 'closed', 'No Motion', 'no_motion']

def get_elapsed_in_milliseconds(from_datetime):
  fixed_from = from_datetime.rsplit(':', 1)[0] + from_datetime.rsplit(':', 1)[1]
  return int((datetime.now(pytz.utc) - datetime.strptime(fixed_from, '%Y-%m-%dT%H:%M:%S.%f%z')).total_seconds() * 1000)

def get_uuid_str():
  return str(uuid4())

def get_iso_datetime_utc_tz_str():
  return str(datetime.utcnow().replace(tzinfo=timezone.utc).isoformat())

def entityId_to_endpointId(entityId):
  return entityId.replace('.', '_', 1)
  
def endpointId_to_entityId(endpointId):
  return endpointId.replace('_', '.', 1)
  
def fix_service_domain(service_name):
  return service_name.replace('.', '/', 1)