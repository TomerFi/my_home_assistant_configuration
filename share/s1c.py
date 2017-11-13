import broadlink
import os
import time
import logging

mosquitto_address = ""
mosquitto_port = ""
mosquitto_user = ""
mosquitto_password = ""
broadlink_s1c_ip = ""
broadlink_s1c_mac = ""

# _LOGGER = logging.getLogger(__name__)
devices = broadlink.S1C(host=(broadlink_s1c_ip, 80), mac=bytearray.fromhex(broadlink_s1c_mac))
devices.auth()


def checkSensor(v_type, v_name, v_status):
    if v_type == "Door Sensor" and v_status in ("0", "128"):
        sendToMosquito(v_name, "Closed")
    elif v_type == "Door Sensor" and v_status in ("16", "144"):
        sendToMosquito(v_name, "Open")
    elif v_type == "Door Sensor" and v_status == "48":
        sendToMosquito(v_name, "Tampered")
    elif v_type == "Motion Sensor" and v_status in ("0", "128"):
        sendToMosquito(v_name, "No_motion")
    elif v_type == "Motion Sensor" and v_status == "16":
        sendToMosquito(v_name, "Motion_Detected")
    elif v_type == "Motion Sensor" and v_status == "32":
        sendToMosquito(v_name, "Tampered")
    return


def sendToMosquito(v_deviceName, v_payload):
    os.system("mosquitto_pub -h " + mosquitto_address + " -p " + mosquitto_port + " -t 'sensors/s1c/" + v_deviceName + "' -u " + mosquitto_user + " -P " + mosquitto_password + " -m " + v_payload)
    return

# _LOGGER.error("started")
# time.sleep(600)
sens = devices.get_sensors_status()
old = sens

for k, se in enumerate(sens['sensors']):
    # _LOGGER.error("found " + se['type'] + " " + se['name'] + " " + str(se['status']))
    checkSensor(se['type'], ((se['name']).replace(" ", "_")).lower(), str(se['status']))

while 1:
    try:
        sens = devices.get_sensors_status()
        for i, se in enumerate(sens['sensors']):
            if se['status'] != old['sensors'][i]['status']:
                # _LOGGER.error("update " + se['type'] + " " + se['name'] + " " + str(se['status']))
                checkSensor(se['type'], ((se['name']).replace(" ", "_")).lower(), str(se['status']))
                old = sens
    except:
        continue
