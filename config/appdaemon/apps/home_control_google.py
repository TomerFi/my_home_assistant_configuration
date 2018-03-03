import appdaemon.appapi as appapi
import home_control as home_control

class HomeControl(appapi.AppDaemon):

    def initialize(self):
        self.handler = self.register_endpoint(self.api_call)

    def api_call(self, data):
        #self.log(data)
        if ("responseId" in data):
            self.v2 = True
            user_id = data["originalDetectIntentRequest"]["payload"]["user"]["userId"]
        else:
            #self.v2 = False
            #user_id = data["originalRequest"]["data"]["user"]["userId"]
            return "", 500

        response = ""
        code = 200

        if not (home_control.authorizeGoogleUse(self, user_id)):
            code = 404
        else:
            intent = self.getIntentName(data)
            try:
                func = getattr(self, intent)
                response = func(data)
            except:
                response = self.tellText(data, home_control.handleUnknownIntentText(self, intent))

        #self.log(response)
        return response, code

    #########################
    ######## Intents ########
    #########################
    def LaunchRequest(self, data):
        prompt, reprompt = home_control.handleLaunchText()
        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "LaunchRequest")
        return response

    def LocatePhoneIntent(self, data):
        selectedProfile, prompt, reprompt = home_control.handleLocateProfileText(self, self.getParameterValue(data, "name").lower() , self.isNewConversation(data))
        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "LocatePhoneIntent")
        self.setSessionAttribute(data, response, "person_profile", selectedProfile)
        return response

    def CancelIntent(self, data):
        prompt, reprompt = home_control.handleCancelText(self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "CancelIntent")
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
        self.setSessionAttribute(data, response, "previous_intent", "NoIntent")
        return response

    def StopIntent(self, data):
        prompt, reprompt = home_control.handleStopText(self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "StopIntent")
        return response

    def YesIntent(self, data):
        prompt, reprompt, title, context = home_control.handleYesCardText(self, self.getSessionAttributes(data))
        if (reprompt is None):
            response = self.tellText(data, prompt)
        else:
            response = self.askText(data, prompt, reprompt)
        
        if not (title is None):
            self.setSimpleCard(response, title, context)
        
        self.setSessionAttribute(data, response, "previous_intent", "YesIntent")
        return response

    def IdentifyIntent(self, data):
        prompt, reprompt = home_control.handleIdentifySsml(self.isNewConversation(data))
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "IdentifyIntent")
        return response

    def SensorsIntent(self, data):
        prompt, reprompt = home_control.handleSensorsText(self, self.isNewConversation(data))
        response = self.askText(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "SensorsIntent")
        return response

    def SystemDataIntent(self, data):
        prompt, reprompt = home_control.handleSystemDataSsml(self, self.isNewConversation(data))
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "SystemDataIntent")
        return response

    def NetworkDataIntent(self, data):
        prompt, reprompt = home_control.handleNetworkSsml(self, self.isNewConversation(data))
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "NetworkDataIntent")
        return response

    def StorageDataIntent(self, data):
        prompt, reprompt = home_control.handleStorageSsml(self, self.isNewConversation(data))
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "StorageDataIntent")
        return response

    def DevicesDataIntent(self, data):
        prompt, reprompt = home_control.handleDevicesSsml(self, self.isNewConversation(data))
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "DevicesDataIntent")
        return response

    def SystemOperationsIntent(self, data):
        prompt, reprompt = home_control.handleSystemOprationsSsml(self.isNewConversation(data))
        response = self.askSSML(data, prompt, reprompt)
        self.setSessionAttribute(data, response, "previous_intent", "SystemOperationsIntent")
        return response

    def BoilerRequestsIntent(self, data):
        attributes = self.getSessionAttributes(data)
        duration = self.getParameterValue(data, "Duration")
        action = self.getParameterValue(data, "Action")
        prompt, reprompt, title, context = home_control.handleBoilerCardSsml(self, attributes, action, duration, self.isNewConversation(data), False)
        self.log(prompt)
        self.log(reprompt)
        if (reprompt is None):
            response = self.tellSSML(data, prompt)
        else:
            response = self.askSSML(data, prompt, reprompt)
        if not (title is None):
            self.setSimpleCard(response, title, context)
        self.setSessionAttribute(data, response, "previous_intent", "BoilerRequestsIntent")
        return response

    #########################
    ######## Helpers ########
    #########################
    def getSessionAttributes(self, data):
        if ("parameters" not in data["queryResult"]):
            return {}
        else:
            return data["queryResult"]["parameters"]

    def setSessionAttribute(self, data, response, key, value):
        existing_context = None
        for context in response["outputContexts"]:
            if (context["name"] ==  data["session"] + "/contexts/custom_data_context"):
                existing_context = context
                break

        if (existing_context is None):
            response["outputContexts"].append(
                {
                    "name": data["session"] + "/contexts/custom_data_context",
                    "lifespanCount": 10,
                    "parameters": {
                        key: value
                    }
                })
        else:
            existing_context["parameters"][key] = value
            response["outputContexts"].append(existing_context)


    def setSimpleCard(self, response, title, content):
        response["fulfillmentMessages"].append(
            {
                "card": {
                    "title": title,
                    "subtitle": content
                }
            })

    def tellText(self, data, prompt):
        response = \
        {
            "fulfillmentText": "Home Assitant",
            "fulfillmentMessages": [
            ],
            "source": "TomerFi Custom",
            "payload": {
            },
            "outputContexts": [
            ],
            "followupEventInput": {
                "name": "END_CONVERSATION",
                "parameters": {
                    "end_prompt": prompt
                },
                "languageCode": "en"
            }
        }
        
        return response

    def askText(self, data, prompt, reprompt):
        response = \
        {
            "fulfillmentText": "Home Assitant",
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simple_responses": {
                        "simple_responses": [
                            {
                                "text_to_speech": prompt,
                                "display_text": prompt
                            }
                        ]
                    }
                }
            ],
            "source": "TomerFi Custom",
            "payload": {
            },
            "outputContexts": [
            ],
            "followupEventInput": {
            }
        }
        
        self.setSessionAttribute(data, response, "reprompt", reprompt)
        return response

    def tellSSML(self, data, prompt):
        response = \
        {
            "fulfillmentText": "Home Assitant",
            "fulfillmentMessages": [
            ],
            "source": "TomerFi Custom",
            "payload": {
            },
            "outputContexts": [
            ],
            "followupEventInput": {
                "name": "END_CONVERSATION",
                "parameters": {
                    "end_prompt": prompt
                },
                "languageCode": "en"
            }
        }

        return response

    def askSSML(self, data, prompt, reprompt):
        response = \
        {
            "fulfillmentText": "Home Assitant",
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simple_responses": {
                        "simple_responses": [
                            {
                                "ssml": prompt,
                                "display_text": prompt
                            }
                        ]
                    }
                }
            ],
            "source": "TomerFi Custom",
            "payload": {
            },
            "outputContexts": [
            ],
            "followupEventInput": {
            }
        }
        self.setSessionAttribute(data, response, "reprompt", reprompt)
        return response

    def isNewConversation(self, data):
        if (self.v2):
            if ("originalDetectIntentRequest" in data and "payload" in data["originalDetectIntentRequest"] and "conversation" in data["originalDetectIntentRequest"]["payload"] and "type" in data["originalDetectIntentRequest"]["payload"]["conversation"]):
                return data["originalDetectIntentRequest"]["payload"]["conversation"]["type"].upper() == "NEW"
            else:
                return False
        else:
            if ("originalRequest" in data and "data" in data["originalRequest"] and "conversation" in data["originalRequest"]["data"] and "type" in data["originalRequest"]["data"]["conversation"]):
                return data["originalRequest"]["data"]["conversation"]["type"].upper() == "NEW"
            else:
                return False


    def getParameterValue(self, data, name):
        if (self.v2):
            if ("queryResult" in data and "parameters" in data["queryResult"] and name in data["queryResult"]["parameters"]):
                return data["queryResult"]["parameters"][name]
            else:
                return None
        else:
            if ("result" in data and "parameters" in data["result"] and name in data["result"]["parameters"]):
                return data["result"]["parameters"][name]
            else:
                return None

    def getIntentName(self, data):
        if (self.v2):
            if ("queryResult" in data and "intent" in data["queryResult"] and "displayName" in data["queryResult"]["intent"]):
                return data["queryResult"]["intent"]["displayName"]
            else:
                return None
        else:
            if ("result" in data and "metadata" in data["result"] and "intentName" in data["result"]["metadata"]):
                return data["result"]["metadata"]["intentName"]
            else:
                return None
