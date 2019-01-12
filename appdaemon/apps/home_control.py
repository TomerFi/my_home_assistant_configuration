import random
import datetime
import user_secrets

start_phrases = [
    "Hello gov'nor!",
    "Top of the mornin’ to ya!",
    "What’s crackin’?",
    "‘Sup...",
    "This call may be recorded for training purposes.",
    "How you been, Jellybean?",
    "Hello, my name is Inigo Montoya.",
    "I'm Batman.",
    "You know who this is.",
    "Ghostbusters,",
    "Yo!",
    "Greetings and salutations!",
    "Doctor.",
    "Hello sunshine!",
    "Howdy partner!",
    "Hey, howdy, hi!",
    "What’s kickin’... little chicken!",
    "Peek-a-boo!",
    "Howdy-doody!",
    "Hey there.",
    "Hi master!",
    "I come in peace!",
    "Ahoy matey!",
    "Aloha!",
    "Hola!",
    "Que pasa!",
    "Bonjour!",
    "Konnichiwa!"
]

end_phrases = [
    "I've got your back! Let me know if you need anything.",
    "Not all goodbyes are sad, for example: Goodbye Class!",
    "It will not be the same without you. It will actually be better!",
    "Farewell. Someone is really going to miss you. But, it is not going to be me!",
    "It won't be the same without you here, work may actually get done!",
    "I am looking forward to not keeping in touch with you! So long!",
    "So long, and thanks for all the fish!",
    "How lucky I am to have something that makes saying Goodbye so hard.",
    "Good friends never say goodbye, they simply say: see you soon!",
    "See ya in a while, crocodile.",
    "Easy-peasy lemon squeezy!",
    "Later, tater!",
    "Elvis, has left the building!",
    "Your personal digital assistant, has left the building!",
    "So long, King Kong.",
    "Take care, teddy bear.",
    "Asta-lavista!",
    "You'll be back. I know, you will...",
    "I, am, outta here.",
    "Don't be a stranger...",
    "Take it easy.",
    "Adios.",
    "See you around.",
    "Take care.",
    "Bye-bye, for now...",
    "Later...",
    "Hurry back.",
    "Till we meet again...",
    "Keep in touch.",
    "Arrivederci!",
    "Ciao!",
    "Nice talking to you.",
    "So long buddy...",
    "I'm here if you need me.",
    "Oops, there I go.",
    "Boom!",
    "I am here for you! Unless you unplug me! In which case: I won't be here, at all!"
]

hava_profile = {
    "update_script": "script.update_hava_devices",
    "tracker_sensor": "sensor.hava_tracker_sensor",
    "names": [
        "hava",
        "my wife"
    ]
}

tomer_profile = {
    "update_script": "script.update_tomer_devices",
    "tracker_sensor": "sensor.tomer_tracker_sensor",
    "names": [
        "tomer",
        "my husband"
    ]
}

door_sensors = [
    "sensor.broadlink_s1c_closet_room",
    "sensor.broadlink_s1c_main_bathroom",
    "sensor.broadlink_s1c_service_room",
    "sensor.broadlink_s1c_small_bathroom",
    "sensor.broadlink_s1c_balcony_door"
]

motion_sensors = [
    "sensor.broadlink_s1c_shower_motion_sensor"
]

system_sensors = {
    "cpu_temp": "sensor.cpu_temp",
    "cpu_used": "sensor.processor_use",
    "last_boot": "sensor.last_boot",
    "disk_used": "sensor.disk_use_percent_home",
    "ram_used": "sensor.memory_use_percent"
}

devices_sensors = [
    "sensor.home_workstation_update_mqtt_client_status",
    "sensor.kitchen_echo_one_nmap_tracker",
    "sensor.living_room_dot_nmap_tracker",
    "sensor.nursery_dot_nmap_tracker",
    "sensor.bedroom_echo_nmap_tracker",
    "sensor.office_dot_nmap_tracker",
    "sensor.living_room_ghome_mini_nmap_tracker",
    "sensor.dash_wand_nmap_tracker",
    "sensor.living_room_rm_pro_nmap_tracker",
    "sensor.bedroom_rm_mini_nmap_tracker",
    "sensor.office_rm_mini_nmap_tracker",
    "sensor.living_room_harmony_hub_nmap_tracker",
    "sensor.living_room_yes_nmap_tracker",
    "sensor.bedroom_yes_nmap_tracker",
    "sensor.guest_room_yes_nmap_tracker",
    "sensor.home_workstation_nmap_tracker",
    "sensor.shield_console_nmap_tracker",
    "sensor.office_chromecast_nmap_tracker",
    "sensor.xbox_360_nmap_tracker",
    "sensor.hue_bridge_nmap_tracker",
    "sensor.nursery_fire_8_tablet_nmap_tracker",
    "sensor.kitchen_fire_8_tablet_nmap_tracker",
    "sensor.tomers_laptop_nmap_tracker",
    "sensor.havas_laptop_nmap_tracker",
    "sensor.tomers_phone_nmap_tracker",
    "sensor.havas_phone_nmap_tracker",
    "sensor.kitchen_bar_sp2_nmap_tracker",
    "sensor.tv_lifxz_led_nmap_tracker",
    "sensor.service_room_s1c_nmap_tracker",
    "sensor.switcher_v2_nmap_tracker",
    "sensor.office_netgear_hub5_nmap_tracker",
    "sensor.nursery_broadlink_a1_nmap_tracker",
    "sensor.living_room_samsung_tv_nmap_tracker",
    "sensor.hallway_rf_gw_nmap_tracker",
    "sensor.office_msensor_nmap_tracker",
    "sensor.bedroom_msensor_nmap_tracker"
]

network_profile = {
    "last_speedtest": "sensor.run_speed_test_last_run",
    "ping_result": "sensor.speedtest_ping",
    "download_result": "sensor.speedtest_download",
    "upload_result": "sensor.speedtest_upload",
    "duckdns_cert": "sensor.ha_duckdns_cert_expiry"
}

storage_profile = {
    "system_status": "sensor.homenas_status",
    "system_temp": "sensor.homenas_system_temperature",
    "cpu_usage": "sensor.homenas_cpu_usage",
    "cpu_temp": "sensor.homenas_cpu_temperature",
    "mem_usage": "sensor.homenas_memory_usage",
    "drive_status": "sensor.homenas_smart_status_drive_01",
    "drive_temp": "sensor.homenas_temperature_drive_01",
    "vol_usage": "sensor.homenas_volume_used_datavol1"
}

water_heater_switch = "switch.heater_switch"

def handleUnknownIntentText(api, intent):
    api.log("unknown intent {}.".format(intent))
    prompt =  "Hmmm... I'm not familiar with the intent {}.".format(intent)

    return prompt

def handleUnknownRequestText(api, requestType):
    api.log("unknown request type {}.".format(requestType))
    prompt =  "Hmmm... I'm not familiar with the request type {}.".format(requestType)

    return prompt

def handleLaunchText():
    prompt = random.choice(start_phrases) +" How can I help you?"
    reprompt = "Not that you need it. But you can ask me for help, if you want..."

    return prompt, reprompt

def handleLocateProfileText(api, name, is_new=False):
    if (name and name in hava_profile["names"]):
        selectedProfile = hava_profile
    elif (name and name in tomer_profile["names"]):
        selectedProfile = tomer_profile
    else:
        api.log("unknown slot value for Name slot {}.".format(name))
        prompt = "Hmmm... I'm not familiar with the name {}, please try again.".format(name)
        reprompt = "If you're not sure, you can ask me for help. I'll do my best to guide you through this."
        return prompt, reprompt

    api.turn_on(selectedProfile["update_script"])
    
    location = api.get_state(selectedProfile["tracker_sensor"]).lower()
    fixed_name = name.replace("my", "your")
    reprompt = "Would you like me to issue a find request?"
    
    if (location == "not_home"):
        prompt = fixed_name + " is not at home. " + reprompt
    else:
        prompt = fixed_name + " is at " + location + ". " + reprompt

    if (is_new):
        prompt = random.choice(start_phrases) + " " + prompt
    
    return selectedProfile, prompt, reprompt

def handleCancelText(attributes):
    prompt = random.choice(end_phrases)
    reprompt = None

    if ("previous_intent" in attributes):
        if (attributes["previous_intent"] == "SystemOperationsIntent"):
            prompt = "You made the right decision! anything else?"
            reprompt = "Anything you need me to do?"
    
    return prompt, reprompt

def handleHelpCardSsml(include_card=False):
    prompt = ("<speak>Try asking me to locate any member of your household, to give you a sensors report or collect hardware data for you." +
        " I can turn the boiler on or off. I can even restart home assistant for you.<break time='200ms'/>Go ahead, try me...</speak>")
    
    reprompt = ("<speak>If you need help configuring what can I do for you, please check Tomer " +
        "<say-as interpret-as='spell-out'>fi</say-as> github repository for further instructions. The link is in a card in your app.</speak>")
    
    if (include_card):
        title = "TomerFi's Github repository"
        content = "https://github.com/TomerFi/appdaemon_hassio_alexa_custom_skill"
        
        return prompt, reprompt, title, content
    else:
        return prompt, reprompt

def handleNoText(attributes):
    prompt = "Hmmm... I'm not quite sure what are you refusing to..."
    reprompt = None

    if ("previous_intent" in attributes):
        if (attributes["previous_intent"] in ["SensorsIntent", "NoIntent", "SystemDataIntent", "NetworkDataIntent", "StorageDataIntent", "DevicesDataIntent", "HandleBoilerRequests", "CancelIntent"]):
            prompt = random.choice(end_phrases)
        elif (attributes["previous_intent"] == "LocatePhoneIntent"):
            prompt = "Ok. anything else?"
            reprompt = "Anything you need me to do?"
        elif (attributes["previous_intent"] == "SystemOperationsIntent"):
            prompt = "whooshhh... dodged a bullet there! anything else?"
            reprompt = "Anything you need me to do?"
    
    return prompt, reprompt

def handleStopText(attributes):
    prompt = "Got it! So... do you need me to do anything for you... or are we just chatting?"
    reprompt = "You know... I can help you... if you want... just ask me for help."

    if ("previous_intent" in attributes):
        if (attributes["previous_intent"] == "StopIntent"):
            prompt = random.choice(end_phrases)
            reprompt = None
    
    return prompt, reprompt

def handleYesCardText(api, attributes):
    prompt = "Hmmm... I'm not quite sure what are you agreeing to..."
    reprompt = None
    title = None
    context = None
    
    if ("previous_intent" in attributes):
        if (attributes["previous_intent"] == "LocatePhoneIntent"):
            api.turn_on(attributes["person_profile"]["find_script"])
            prompt = "Ok. I've issued the find request. If it doesn't ring within the next couple of seconds, holler at me. We'll figure it out together."
        elif (attributes["previous_intent"] in ["SensorsIntent", "NoIntent"]):
            prompt = "Ok. Let's go."
            reprompt = "I'm waiting..."
        elif (attributes["previous_intent"] in ["SystemDataIntent", "NetworkDataIntent", "StorageDataIntent", "DevicesDataIntent"]):
            prompt = "What data do you want me to collect? system, network, storage, or devices data?"
            reprompt = "Are you there?"
        elif (attributes["previous_intent"] == "SystemOperationsIntent"):
            api.call_service("script/turn_on", entity_id = "script.alexa_restart_hass")
            prompt = "OK. I've sent the restart request to Home Assistant... I'm crossing my fingers... If I won't make it... please tell my parents at Amazon, that I loved them! "
            title = "System Restart Request"
            context = "Home Assistant system restart request was sent."
        elif (attributes["previous_intent"] == "BoilerRequestsIntent"):
            prompt = "What is it you need me to do?"
            reprompt = "Take your time..."
    
    return prompt, reprompt, title, context

def handleIdentifySsml(is_new=False):
    prompt = ("Let me tell you a little bit about myself. I'm a custom skill designed to help you control and monitor your Home Assistant environment." +
    " I can check stuff out for you<break time='200ms'/>, I can preform actions on your behalf, <break time='200ms'/>" +
    " and I can report back you with text supporting <say-as interpret-as='spell-out'>ssml</say-as> tags. <break time='200ms'/>What can I do for you?</speak>")
    
    if (is_new):
        prompt = "<speak>" + random.choice(start_phrases) + " " + prompt
    else:
        prompt = "<speak>" + prompt
    
    reprompt = "<speak>What is it you need me to do for you? If you're not sure, you can ask me for help.</speak>"
    
    return prompt, reprompt

def handleSensorsText(api, is_new=False):
    prompt = ""
    reprompt = "Anything else I can do for you?"

    for sensor in door_sensors:
        if (api.get_state(sensor).lower() == "open"):
            prompt = prompt + "The " + api.get_state(sensor, attribute="friendly_name") + ", "
    
    if (prompt != ""):
        prompt = "The following door sensors appear to be open: " + prompt[:-2] + " "
    else:
        prompt = "All the door sensors appear to be closed. "

    motion_sensor_prompt = ""
    for sensor in motion_sensors:
    	if (api.get_state(sensor).lower() == "motion_detected"):
    		motion_sensor_prompt = motion_sensor_prompt = "" +  api.get_state(sensor, attribute="friendly_name") + ", "

    if (motion_sensor_prompt != ""):
        prompt = prompt + ". The following motion sensors are detecting motion: " + motion_sensor_prompt[:-2] + ". And... well, that's it! " + reprompt
    else:
        prompt = prompt + ". There is no motion detected in any of the motion sensors. " + reprompt
    
    if (is_new):
        prompt = random.choice(start_phrases) + " " + prompt
    
    return prompt, reprompt

def handleSystemDataSsml(api, is_new=False):
    cpu_temp = api.get_state(system_sensors["cpu_temp"])
    cpu_used = api.get_state(system_sensors["cpu_used"])
    last_boot = api.get_state(system_sensors["last_boot"])
    disk_used = api.get_state(system_sensors["disk_used"])
    ram_used = api.get_state(system_sensors["ram_used"])
    
    prompt = ("<p>I've collected the following system data:</p>" +
        "<p>The <say-as interpret-as='spell-out'>cpu</say-as> temperature is: " +
        cpu_temp + "celsius degrees. And its usage is: " + cpu_used + " percent.</p>" +
        "<p>The disk usage is: " + disk_used + " percent.</p>" +
        "<p>The ram usage is: " + ram_used + " percent.</p>" +
        "<p>The last system restart was on <say-as interpret-as='date' format='ymd'>" + last_boot +
        "</say-as>.</p>Do you need me to collect extra data?</speak>")
    
    reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"
    
    if (is_new):
        prompt = "<speak>" + random.choice(start_phrases) + " " + prompt
    else:
        prompt = "<speak>" + prompt
    
    return prompt, reprompt

def handleNetworkSsml(api, is_new=False):
    last_speedtest = api.get_state(network_profile["last_speedtest"])
    ping_result = api.get_state(network_profile["ping_result"])
    download_result = api.get_state(network_profile["download_result"])
    upload_result = api.get_state(network_profile["upload_result"])
    duckdns_cert = api.get_state(network_profile["duckdns_cert"])

    dt = last_speedtest.split(" ")

    if (datetime.datetime.strptime(dt[0], '%Y-%m-%d') == datetime.date.today()):
        test_date = "today at "
    else:
        test_date = "on " + dt[0] + " at "

    time = dt[1].split(":")[0] + ":" + dt[1].split(":")[1]

    prompt = ("<p>I've collected the following network data:</p>" + 
        "<p>The last speed test was performed " + test_date + time +
        ". The ping result was: " + ping_result + " milliseconds." +
        " The download result was: " + download_result + " mega-bit per second." +
        " The upload result was: " + upload_result + " mega-bit per second.</p>" +
        "<p>Your Duck <say-as interpret-as='spell-out'>dns</say-as> certification renewal is in " + duckdns_cert + " days.</p>" +
        "Do you need me to collect extra data?</speak>")

    reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"
    
    if (is_new):
        prompt = "<speak>" + random.choice(start_phrases) + " " + prompt
    else:
        prompt = "<speak>" + prompt

    return prompt, reprompt

def handleStorageSsml(api, is_new=False):
    system_status = api.get_state(storage_profile["system_status"])
    system_temp = api.get_state(storage_profile["system_temp"])
    cpu_usage = api.get_state(storage_profile["cpu_usage"])
    cpu_temp = api.get_state(storage_profile["cpu_temp"])
    mem_usage = api.get_state(storage_profile["mem_usage"])
    drive_status = api.get_state(storage_profile["drive_status"])
    drive_temp = api.get_state(storage_profile["drive_temp"])
    vol_usage = api.get_state(storage_profile["vol_usage"])

    prompt = ("<p>I've collected the following storage data from your nas:</p>" +
        "<p>The system's status is: " + system_status + ", and its temperature is: " + system_temp + "celsius degrees.</p>" +
        "<p>The <say-as interpret-as='spell-out'>cpu</say-as> temperature is: " + cpu_temp +
        "celsius degrees. And its usage is: " + cpu_usage + " percent.</p>" +
        "<p>The drive status is: " + drive_status + ", and its temperature is: " + drive_temp + "celsius degrees.</p>" +
        "<p>The memory usage is: " + mem_usage + " percent.</p>" +
        "<p> The volume usage is: " + vol_usage + " percent.</p>"+
        "Do you need me to collect extra data?</speak>")

    reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"

    if (is_new):
        prompt = "<speak>" + random.choice(start_phrases) + " " + prompt
    else:
        prompt = "<speak>" + prompt

    return prompt, reprompt

def handleDevicesSsml(api, is_new=False):
    prompt = ""
    count = 0
    
    for sensor in devices_sensors:
        if (api.get_state(sensor).lower() != "online"):
            count = count + 1
            prompt = prompt + api.get_state(sensor, attribute="friendly_name") + ", "

    if (count == 0):
        prompt = "Everything is Online, we're good! anything else you want me to check?"
    elif (count == 1):
        prompt = "<p>" "One device appears be Offline:</p><p>" + prompt[:-2] + ".</p>"
    else:
        prompt = "<p>" + str(count) + " devices appears be Offline:</p><p>" + prompt[:-2] + ".</p>"

    
    if (is_new):
        prompt = "<speak>" + random.choice(start_phrases) + " " + prompt + "Do you need me to collect extra data?</speak>"
    else:
        prompt = "<speak>" + prompt + "Do you need me to collect extra data?</speak>"

    reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"

    return prompt, reprompt

def handleSystemOprationsSsml(is_new=False):
    prompt = "hmmm... A System reboot?! are you sure?! If the system fails to restart, I won't be here to help you figure it out...</speak>"

    if (is_new):
        prompt = "<speak>" + random.choice(start_phrases) + " " + prompt
    else:
        prompt = "<speak>" + prompt

    reprompt = "<speak>So... should I reboot? You can say no, I won't be mad.</speak>"
    
    return prompt, reprompt

def handleBoilerCardSsml(api, attributes, action, duration, is_new=False, is_iso_duration=True):
    prompt = ""
    reprompt = None
    title = None
    content = None

    if ("previous_intent" in attributes and attributes["previous_intent"] == "BoilerRequestsIntent" and (action is None or action == "")):
        action = "start"
    else:
        action = action.lower()

    if (action == "" or action is None):
        prompt = "hmmm... I'not quite sure what you are asking me to do. Try asking me to turn on, off, start or stop the boiler.</speak>"
        
        if (is_new):
            prompt = "<speak>" + random.choice(start_phrases) + " " + prompt
        else:
            prompt = "<speak>" + prompt

        reprompt = "<speak>Hello... Are you there?</speak>"
        

    if (action == "stop" or action == "off" or action == "close"):
        api.call_service("switch/turn_off", entity_id = water_heater_switch)
        
        prompt = "<speak>Done. Anything else I can do for you?</speak>"
        reprompt = "<speak>hmmm... are you gonna... or should I, just...</speak>"

    if (duration == "" or duration is None):
        prompt = "<speak>For how long?</speak>"
        reprompt = "<speak>I can turn on the boiler for any number of minutes up to 60, how long do you want me to turn on the boiler for?</speak>"
    else:
        if (is_iso_duration):
            seconds = convertISODurationToSeconds(duration)
        else:
            seconds = convertObjectDurationToSeconds(duration)

        api.log(str(seconds))
        if (seconds < 10 or seconds > 3600):
            prompt =  "<speak>I can schedule the boiler to turn off anywhere between 1 and 60 minutes. How long do you want me to turn it on for?</speak>"
            reprompt = "<speak>I can turn on the boiler for any number of minutes up to 60, how long do you want me to turn on the boiler for?</speak>"
        else:
            api.call_service("switch/turn_on", entity_id = water_heater_switch)
            api.run_in(boilerTurnOffCallback, seconds, api=api, entity_id=water_heater_switch)

            time = str(datetime.timedelta(seconds=seconds))

            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[1])
            seconds = int(time.split(':')[2])

            timeSpeech = ""
            
            if hours == 1:
                timeSpeech = "one hour"
            elif hours > 1:
                timeSpeech = str(hours) + " hours"

            if minutes == 1:
                if timeSpeech == "":
                    timeSpeech = "one minute"
                else:
                    timeSpeech = timeSpeech + " and one minute"
            elif minutes > 1:
                if timeSpeech == "":
                    timeSpeech = str(minutes) + " minutes"
                else:
                    timeSpeech = timeSpeech + " and " + str(minutes) + " minutes"

            if seconds == 1:
                if timeSpeech == "":
                    timeSpeech = "one second"
                else:
                    timeSpeech = timeSpeech + " and one second"
            elif seconds > 1:
                if timeSpeech == "":
                    timeSpeech = str(seconds) + " seconds"
                else:
                    timeSpeech = timeSpeech + " and " + str(seconds) + " seconds"

            prompt = "<speak>Done. The boiler is turned on. I'll turn it off in " + timeSpeech + ". " + random.choice(end_phrases) + "</speak>"
            title = "Boiler turned on"
            content = "Boiler turned on for " + time + "."

    return prompt, reprompt, title, content

def convertISODurationToSeconds(duration):
    seconds = 0
    if not (duration.split('T')[0] == "P"):
        return seconds

    try:
        dur = duration[2:]

        idx = dur.find('H')
        if idx > -1:
            seconds = seconds + (int(dur[:idx]) * 3600)
            dur = dur[idx+1:]

        idx = dur.find('M')
        if idx > -1:
            seconds = seconds + (int(dur[:idx]) * 60)
            dur = dur[idx+1:]

        idx = dur.find('S')
        if idx > -1:
            seconds = seconds + int(dur[:idx])
    except:
        pass

    return seconds

def convertObjectDurationToSeconds(duration):
    seconds = 0

    if (duration["unit"] == "s"):
        seconds = int(duration["amount"])
    elif (duration["unit"] == "min"):
        seconds = (int(duration["amount"]) * 60)
    elif (duration["unit"] == "h"):
        seconds = (int(duration["amount"]) * 3600)

    return seconds

def boilerTurnOffCallback(args):
    args["api"].call_service("switch/turn_off", entity_id = args["entity_id"])

def authorizeAlexaUse(api, application_id, device_id, user_id):
    authorized = True
    debug = False # set to True to cancel restrictions

    if not (debug):
        # users_secrets.alexa_application_ids is a list of all permitted application ids
        if (not (user_secrets.alexa_application_ids == []) and application_id not in user_secrets.alexa_application_ids):
            api.log("unauthorized application id: {}.".format(application_id))
            authorized = False

        # users_secrets.alexa_device_ids is a list of all permitted device ids
        if (not (user_secrets.alexa_device_ids == [])and device_id  not in user_secrets.alexa_device_ids):
            api.log("unauthorized device id: {}.".format(device_id))
            authorized = False
        
        # users_secrets.alexa_user_ids is a list of all permitted user ids
        if (not (user_secrets.alexa_user_ids == []) and user_id not in user_secrets.alexa_user_ids):
            api.log("unauthorized user id: {}.".format(user_id))
            authorized = False

    return authorized

def authorizeGoogleUse(api, user_id):
    authorized = True
    debug = False # set to True to cancel restrictions

    if not (debug):
        # users_secrets.google_user_ids is a list of all permitted user ids
        if (not (users_secrets.google_user_ids == []) and user_id not in users_secrets.google_user_ids):
            api.log("unauthorized user id: {}.".format(user_id))
            authorized = False

    return authorized
