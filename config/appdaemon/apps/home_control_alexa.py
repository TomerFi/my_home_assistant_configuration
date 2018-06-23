import appdaemon.plugins.hass.hassapi as hassapi
import home_control as home_control

class HomeControl(hassapi.Hass):

    def initialize(self):
        self.handler = self.register_endpoint(self.api_call)

    def api_call(self, data):
        application_id = data["context"]["System"]["application"]["applicationId"]
        device_id = data["context"]["System"]["device"]["deviceId"]
        user_id = data["context"]["System"]["user"]["userId"]

        response = ""
        code = 200

        if not (home_control.authorizeAlexaUse(self, application_id, device_id, user_id)):
            code = 404
        else:
            requestType = data["request"]["type"]

            if (requestType == "LaunchRequest"):
                response = self.LaunchRequest(data)
            elif (requestType == "IntentRequest"):
                intent = self.get_alexa_intent(data).replace("AMAZON.", "")
                try:
                    func = getattr(self, intent)
                    response = func(data)
                except Exception as ex:
                    print(ex)
                    response = self.tellText(data, home_control.handleUnknownIntentText(self, intent))
            elif (requestType == "SessionEndedRequest"):
                if (data["request"]["reason"] == "error"):
                    self.log("Alexa error encountered: {}".format(self.get_alexa_error(data)))
            else:
                response = self.tellText(data, home_control.handleUnknownRequestText(self, requestType))

        return response, code

    #########################
    ######## Intents ########
    #########################
    def LaunchRequest(self, data):
        prompt, reprompt = home_control.handleLaunchText()
        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "LaunchRequest")
        return response

    def LocatePhoneIntent(self, data):
        selectedProfile, prompt, reprompt = home_control.handleLocateProfileText(self, self.get_alexa_slot_value(data, "Name").lower(), data["session"]["new"])
        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "LocatePhoneIntent")
        self.setSessionAttribute(response, "person_profile", selectedProfile)
        return response

    def CancelIntent(self, data):
        prompt, reprompt = home_control.handleCancelText(self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "CancelIntent")
        return response

    def HelpIntent(self, data):
        prompt, reprompt, title, content = home_control.handleHelpCardSsml(True)
        response = self.askSSML(data, prompt, reprompt)
        self.setSimpleCard(response, title, content)
        return response

    def NoIntent(self, data):
        prompt, reprompt = home_control.handleNoText(self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "NoIntent")
        return response

    def StopIntent(self, data):
        prompt, reprompt = home_control.handleStopText(self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "StopIntent")
        return response

    def YesIntent(self, data):
        prompt, reprompt, title, context = home_control.handleYesCardText(self, self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = self.askText(data, prompt, reprompt)
        
        if not (title is None):
            self.setSimpleCard(response, title, context)
        
        self.setSessionAttribute(response, "previous_intent", "YesIntent")
        return response

    def IdentifyIntent(self, data):
        prompt, reprompt = home_control.handleIdentifySsml(data["session"]["new"])
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "IdentifyIntent")
        return response

    def SensorsIntent(self, data):
        prompt, reprompt = home_control.handleSensorsText(self, data["session"]["new"])
        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "SensorsIntent")
        return response

    def SystemDataIntent(self, data):
        prompt, reprompt = home_control.handleSystemDataSsml(self, data["session"]["new"])
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "SystemDataIntent")
        return response

    def NetworkDataIntent(self, data):
        prompt, reprompt = home_control.handleNetworkSsml(self, data["session"]["new"])
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "NetworkDataIntent")
        return response

    def StorageDataIntent(self, data):
        prompt, reprompt = home_control.handleStorageSsml(self, data["session"]["new"])
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "StorageDataIntent")
        return response

    def DevicesDataIntent(self, data):
        prompt, reprompt = home_control.handleDevicesSsml(self, data["session"]["new"])
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "DevicesDataIntent")
        return response

    def SystemOperationsIntent(self, data):
        prompt, reprompt = home_control.handleSystemOprationsSsml(data["session"]["new"])
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(response, "previous_intent", "SystemOperationsIntent")
        return response

    def BoilerRequestsIntent(self, data):
        attributes = self.getSessionAttributes(data)
        duration = self.get_alexa_slot_value(data, "Duration")
        action = self.get_alexa_slot_value(data, "Action")
        prompt, reprompt, title, context = home_control.handleBoilerCardSsml(self, attributes, action, duration, data["session"]["new"], True)
        if (reprompt is None):
            response = self.tellSSML(data, prompt)
        else:
            response = self.askSSML(data, prompt, reprompt)
        if not (title is None):
            self.setSimpleCard(response, title, context)
        self.setSessionAttribute(response, "previous_intent", "BoilerRequestsIntent")
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
