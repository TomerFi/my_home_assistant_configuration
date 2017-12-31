import appdaemon.appapi as appapi
import random
import datetime

class HomeControl(appapi.AppDaemon):

    def initialize(self):
        self.register_endpoint(self.api_call)

    def api_call(self, data):
        allowedApplications = []
        allowedDevices = []
        allowedUsers = []

        applicationId = data["context"]["System"]["application"]["applicationId"]
        if ("deviceId" in data["context"]["System"]["device"]):
            deviceId = data["context"]["System"]["device"]["deviceId"]
        else:
            deviceId = None

        userId = data["context"]["System"]["user"]["userId"]

        if (allowedApplications and applicationId not in allowedApplications):
            self.log("unauthorized applicationId {}.".format(applicationId))
            return "", 404

        if (allowedDevices and deviceId and deviceId not in allowedDevices):
            self.log("unauthorized applicationId {}.".format(applicationId))
            return "", 404

        if (allowedUsers and userId not in allowedUsers):
            self.log("unauthorized applicationId {}.".format(applicationId))
            return "", 404


        requestType = data["request"]["type"]

        if (requestType == "LaunchRequest"):
            response = self.LaunchRequest(data)
            return response, 200

        elif (requestType == "IntentRequest"):
            intent = self.get_alexa_intent(data)

            intents = {
                "LocatePhoneIntent": self.LocatePhoneIntent,
                "AMAZON.CancelIntent": self.CancelIntent,
                "AMAZON.HelpIntent": self.HelpIntent,
                "AMAZON.NoIntent": self.NoIntent,
                "AMAZON.StopIntent": self.StopIntent,
                "AMAZON.YesIntent": self.YesIntent,
                "IdentifyIntent": self.IdentifyIntent,
                "SensorsIntent": self.SensorsIntent,
                "SystemDataIntent": self.SystemDataIntent,
                "NetworkDataIntent": self.NetworkDataIntent,
                "StorageDataIntent": self.StorageDataIntent,
                "DevicesDataIntent": self.DevicesDataIntent,
                "SystemOperationsIntent": self.SystemOperationsIntent
            }

            if intent in intents:
                response = intents[intent](data)
            else:
                self.log("unknown intent {}.".format(intent))
                response = self.tellText(data, "Hmmm... I'm not familiar with the intent {}.".format(intent))

            return response, 200

        elif (requestType == "SessionEndedRequest"):
            if (data["request"]["reason"] == "error"):
                self.log("Alexa error encountered: {}".format(self.get_alexa_error(data)))

        else:
            self.log("unknown request type {}.".format(requestType))
            response = self.tellText(data, "Hmmm... I'm not familiar with the request type {}.".format(requestType))
            return response, 200

    #########################
    ######## Intents ########
    #########################
    def LaunchRequest(self, data):
        return self.askText(data, random.choice(self.args["startPhrases"])+" How can I help you?", "Not that you need it. But you can ask me for help, if you want...")

    def LocatePhoneIntent(self, data):
        slotValue = self.get_alexa_slot_value(data, "Name").lower()

        if (slotValue and slotValue in self.args["havaProfile"]["names"]):
            selectedProfile = self.args["havaProfile"]
        elif (slotValue and slotValue in self.args["tomerProfile"]["names"]):
            selectedProfile = self.args["tomerProfile"]
        else:
            self.log("unknown slot value for Name slot {}.".format(slotValue))
            return self.askText(data, "Hmmm... I'm not familiar with the name {}, please try again.".format(slotValue),
                "If you're not sure, you can ask me for help. I'll do my best to guide you through this.")

        self.turn_on(selectedProfile["update_script"])
        location = self.get_state(selectedProfile["tracker_sensor"]).lower()

        name = slotValue.replace("my", "your")

        reprompt = "Would you like me to issue a find request?"

        if (location == "not_home"):
            prompt = name + " is not at home. " + reprompt
        else:
            prompt = name + " is at " + location + ". " + reprompt

        if (data["session"]["new"]):
            prompt = random.choice(self.args["startPhrases"]) + " " + prompt

        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "LocatePhoneIntent")
        self.setSessionAttribute(response, "person_profile", selectedProfile)

        return response

    def CancelIntent(self, data):
        response = self.tellText(data, random.choice(self.args["endPhrases"]))
        attributes = self.getSessionAttributes(data)
        if ("previous_intent" in attributes):
            if (attributes["previous_intent"] == "SystemOperationsIntent"):
                response = self.askText(data, "You made the right decision! anything else?", "Anything you need me to do?")
            
        return response

    def HelpIntent(self, data):
        response = self.askSSML(data, "<speak>Try asking me to locate any member of your household, to give you a sensors report or collect hardware data for you. I can even restart home assistant for you.<break time='200ms'/>Go ahead, try me...</speak>",
            "<speak>If you need help configuring what can I do for you, please check Tomer <say-as interpret-as='spell-out'>fi</say-as> github repository for further instructions."+
            " The link is in a card in your alexa app.</speak>")

        self.setSimpleCard(response, "TomerFi's Github repository", "https://github.com/TomerFi/appdaemon_hassio_alexa_custom_skill")

        return response

    def NoIntent(self, data):
        response = self.tellText(data, "Hmmm... I'm not quite sure what are you refusing to...")
        attributes = self.getSessionAttributes(data)
        if ("previous_intent" in attributes):
            if (attributes["previous_intent"] in ["SensorsIntent", "NoIntent", "SystemDataIntent", "NetworkDataIntent", "StorageDataIntent", "DevicesDataIntent"]):
                 response = self.tellText(data, random.choice(self.args["endPhrases"]))
            elif (attributes["previous_intent"] == "LocatePhoneIntent"):
                response = self.askText(data, "Ok. anything else?", "Anything you need me to do?")
                self.setSessionAttribute(response, "previous_intent", "NoIntent")
            elif (attributes["previous_intent"] == "SystemOperationsIntent"):
                response = self.askText(data, "whooshhh... dodged a bullet there! anything else?", "Anything you need me to do?")
                self.setSessionAttribute(response, "previous_intent", "NoIntent")

        return response

    def StopIntent(self, data):
        attributes = self.getSessionAttributes(data)
        if ("previous_intent" in attributes and attributes["previous_intent"] == "StopIntent"):
            response = self.tellText(data, random.choice(self.args["endPhrases"]))
        else:
            response = self.askText(data, "Got it! So... do you need me to do anything for you... or are we just chatting?",
                "You know... I can help you... if you want... just ask me for help.")
            self.setSessionAttribute(response, "previous_intent", "StopIntent")
        
        return response


    def YesIntent(self, data):
        response = self.tellText(data, "Hmmm... I'm not quite sure what are you agreeing to...")
        attributes = self.getSessionAttributes(data)
        if ("previous_intent" in attributes):
            if (attributes["previous_intent"] == "LocatePhoneIntent"):
                self.turn_on(attributes["person_profile"]["find_script"])
                response = self.tellText(data, "Ok. I've issued the find request. If it doesn't ring within the next couple of seconds, holler at me. We'll figure it out together.")
            elif (attributes["previous_intent"] == "SensorsIntent"):
                response = self.askText(data, "Ok. Let's go.", "I'm waiting...")
            elif (attributes["previous_intent"] in ["SystemDataIntent", "NetworkDataIntent", "StorageDataIntent", "DevicesDataIntent"]):
                response = self.askText(data, "What data do you want me to collect? system, network, storage, or devices data?", "Are you there?")
            elif (attributes["previous_intent"] == "SystemOperationsIntent"):
                self.call_service("script/turn_on", entity_id = "script.alexa_restart_hass")
                response = self.tellText(data, "OK. I've sent the restart request to Home Assistant... I'm crossing my fingers... If I won't make it... please tell my parents at Amazon, that I loved them! ")
                self.setSimpleCard(response, "System Restart Request", "Home Assistant system restart request was sent.")

        return response

    def IdentifyIntent(self, data):
        prompt = ("Let me tell you a little bit about myself. I'm a custom skill designed to help you control and monitor your Home Assistant environment." +
        " I can check stuff out for you<break time='200ms'/>, I can preform actions on your behalf, <break time='200ms'/>" +
        " and I can report back you with text supporting <say-as interpret-as='spell-out'>ssml</say-as> tags. <break time='200ms'/>What can I do for you?</speak>")

        if (data["session"]["new"]):
            prompt = "<speak>" + random.choice(self.args["startPhrases"]) + " " + prompt
        else:
            prompt = "<speak>" + prompt

        return self.askSSML(data, prompt, "<speak>What is it you need me to do for you? If you're not sure, you can ask me for help.</speak>")

    def SensorsIntent(self, data):
        prompt = ""
        reprompt = "Anything else I can do for you?"
        for sensor in self.args["doorSensors"]:
            if (self.get_state(sensor).lower() == "open"):
                prompt = prompt + "The " + self.get_state(sensor, "friendly_name") + ", "

        if (prompt != ""):
            prompt = "The following sensors appear to be open: " + prompt[:-2] + ". And... well, that's it!" + reprompt
        else:
            prompt = "All the sensors appear to be closed. " + reprompt

        if (data["session"]["new"]):
            prompt = random.choice(self.args["startPhrases"]) + " " + prompt

        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "SensorsIntent")

        return response

    def SystemDataIntent(self, data):
        cpu_temp = self.get_state(self.args["system_sensors"]["cpu_temp"])
        cpu_used = self.get_state(self.args["system_sensors"]["cpu_used"])
        last_boot = self.get_state(self.args["system_sensors"]["last_boot"])
        disk_used = self.get_state(self.args["system_sensors"]["disk_used"])
        ram_used = self.get_state(self.args["system_sensors"]["ram_used"])

        prompt = ("<p>I've collected the following system data:</p>" +
            "<p>The <say-as interpret-as='spell-out'>cpu</say-as> temperature is: " +
            cpu_temp + "celsius degrees. And its usage is: " + cpu_used + " percent.</p>" +
            "<p>The disk usage is: " + disk_used + " percent.</p>" +
            "<p>The ram usage is: " + ram_used + " percent.</p>" +
            "<p>The last system restart was on <say-as interpret-as='date' format='ymd'>" + last_boot +
            "</say-as>.</p>Do you need me to collect extra data?</speak>")

        reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"

        if (data["session"]["new"]):
            prompt = "<speak>" + random.choice(self.args["startPhrases"]) + " " + prompt
        else:
            prompt = "<speak>" + prompt

        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "SystemDataIntent")

        return response

    def NetworkDataIntent(self, data):
        last_speedtest = self.get_state(self.args["network_profile"]["last_speedtest"])
        ping_result = self.get_state(self.args["network_profile"]["ping_result"])
        download_result = self.get_state(self.args["network_profile"]["download_result"])
        upload_result = self.get_state(self.args["network_profile"]["upload_result"])
        duckdns_cert = self.get_state(self.args["network_profile"]["duckdns_cert"])
        noip_cert = self.get_state(self.args["network_profile"]["noip_cert"])

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
            "<p>Your no <say-as interpret-as='spell-out'>ip</say-as> certification renewal is in " + noip_cert + "days.</p>" +
            "Do you need me to collect extra data?</speak>")

        reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"
        
        if (data["session"]["new"]):
            prompt = "<speak>" + random.choice(self.args["startPhrases"]) + " " + prompt
        else:
            prompt = "<speak>" + prompt

        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "NetworkDataIntent")
        return response

    def StorageDataIntent(self, data):
        system_status = self.get_state(self.args["storage_profile"]["system_status"])
        system_temp = self.get_state(self.args["storage_profile"]["system_temp"])
        cpu_usage = self.get_state(self.args["storage_profile"]["cpu_usage"])
        cpu_temp = self.get_state(self.args["storage_profile"]["cpu_temp"])
        mem_usage = self.get_state(self.args["storage_profile"]["mem_usage"])
        drive_status = self.get_state(self.args["storage_profile"]["drive_status"])
        drive_temp = self.get_state(self.args["storage_profile"]["drive_temp"])
        vol_usage = self.get_state(self.args["storage_profile"]["vol_usage"])

        prompt = ("<p>I've collected the following storage data from your nas:</p>" +
            "<p>The system's status is: " + system_status + ", and its temperature is: " + system_temp + "celsius degrees.</p>" +
            "<p>The <say-as interpret-as='spell-out'>cpu</say-as> temperature is: " + cpu_temp +
            "celsius degrees. And its usage is: " + cpu_usage + " percent.</p>" +
            "<p>The drive status is: " + drive_status + ", and its temperature is: " + drive_temp + "celsius degrees.</p>" +
            "<p>The memory usage is: " + mem_usage + " percent.</p>" +
            "<p> The volume usage is: " + vol_usage + " percent.</p>"+
            "Do you need me to collect extra data?</speak>")

        reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"

        if (data["session"]["new"]):
            prompt = "<speak>" + random.choice(self.args["startPhrases"]) + " " + prompt
        else:
            prompt = "<speak>" + prompt

        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "StorageDataIntent")
        return response

    def DevicesDataIntent(self, data):
        prompt = ""
        count = 0
        for sensor in self.args["devices_sensors"]:
            if (self.get_state(sensor).lower() != "online"):
                count = count + 1
                prompt = prompt + self.get_state(sensor, "friendly_name") + ", "

        if (count == 0):
            prompt = "Everything is Online, we're good! anything else you want me to check?"
        elif (count == 1):
            prompt = "<p>" "One device appears be Offline:</p><p>" + prompt[:-2] + ".</p>"
        else:
            prompt = "<p>" + str(count) + " devices appears be Offline:</p><p>" + prompt[:-2] + ".</p>"

        
        if (data["session"]["new"]):
            prompt = "<speak>" + random.choice(self.args["startPhrases"]) + " " + prompt + "Do you need me to collect extra data?</speak>"
        else:
            prompt = "<speak>" + prompt + "Do you need me to collect extra data?</speak>"

        reprompt = "<speak>I can collect system, network, storage and devices data. I can even restart the system, if you think it's a good idea. Anything I can interest you with?</speak>"

        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "DevicesDataIntent")
        return response

    def SystemOperationsIntent(self, data):
        prompt = "hmmm... A System reboot?! are you sure?! If the system fails to restart, I won't be here to help you figure it out...</speak>"

        if (data["session"]["new"]):
            prompt = "<speak>" + random.choice(self.args["startPhrases"]) + " " + prompt
        else:
            prompt = "<speak>" + prompt

        reprompt = "<speak>So... should I reboot? You can say no, I won't be mad.</speak>"
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "SystemOperationsIntent")
        return response

    #########################
    ######## Helpers ########
    #########################
    def getSessionAttributes(self, data):
        if ("attributes" not in data["session"]):
            return {}
        else:
            return data["session"]["attributes"]

    def setSessionAttribute(self, response, key, value):
        response["sessionAttributes"][key] = value

    def setSimpleCard(self, response, title, content):
        response["response"]["card"] = {
            "type": "Simple",
            "title": title,
            "content": content
        }

    def setStandardCard(self, response, title, text, smallImageUrl, largeImageUrl):
        response["response"]["card"] = {
            "type": "Standard",
            "title": title,
            "text": text,
            "image": {
                "smallImageUrl": smallImageUrl,
                "largeImageUrl": largeImageUrl
            }
        }

    def tellText(self, data, prompt):
            response = {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": prompt
                },
                "shouldEndSession": True
            }

            sessionAttributes = self.getSessionAttributes(data)

            return {
                "version": "1.0",
                "response": response,
                "sessionAttributes": sessionAttributes
            }

    def askText(self, data, prompt, reprompt):
            response = {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": prompt
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": reprompt
                    }
                },
                "shouldEndSession": False
            }

            sessionAttributes = self.getSessionAttributes(data)

            return {
                "version": "1.0",
                "response": response,
                "sessionAttributes": sessionAttributes
            }

    def tellSSML(self, data, prompt):
            response = {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": prompt
                },
                "shouldEndSession": True
            }

            sessionAttributes = self.getSessionAttributes(data)

            return {
                "version": "1.0",
                "response": response,
                "sessionAttributes": sessionAttributes
            }

    def askSSML(self, data, prompt, reprompt):
            response = {
                "outputSpeech": {
                    "type": "SSML",
                    "ssml": prompt
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "SSML",
                        "ssml": reprompt
                    }
                },
                "shouldEndSession": False
            }

            sessionAttributes = self.getSessionAttributes(data)

            return {
                "version": "1.0",
                "response": response,
                "sessionAttributes": sessionAttributes
            }
