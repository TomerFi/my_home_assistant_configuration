# My  Home Assistant Configuration
This is my home assistant configruation, although I'm going to focus on home assistat, I'll also talk about my smart home devices and my alexa configuration in order to fully describe my smart home.</br>
I will try to keep this repository updated with any changes I'll make in my working environment as much as I can.

**Table Of Contents**
- [Home Assistant](#home-assistant)
  - [Customization and modification](#customization-and-modification)
    - [Custom Addons](#custom-addons)
    - [Custom Components](#custom-components)
    - [Python Scripts](#python-scripts)
  - [Themes](#themes)
  - [Installed Hass.io Addons](#installed-hassio-addons)
  - [Frontend](#frontend)
- [Network Gear](#network-gear)
- [Smart Home Devices, Equipment and Endpoints](#smart-home-devices-equipment-and-endpoints)
- [Alexa Skills Configuration](#alexa-skills-configuration)
- [Useful Tools and Applications](#useful-tools-and-applications)

## Home Assistant

### Customization and modification

#### Custom Addons
- [**s1c**](addons/s1c) build based on [this post](https://community.home-assistant.io/t/broadlink-s1c-kit-sensors-in-ha-using-python-and-mqtt/19886/23). The files in the [*share*](share) folder are related to this addon.

#### Custom Components
- [**variable**](config/custom_components/variable.py) as instructed in [this post](https://community.home-assistant.io/t/custom-component-to-declare-set-variables/25218).
- [**sensor/google_geocode**](config/custom_components/sensor/google_geocode.py) as instructed in [this post](https://community.home-assistant.io/t/google-geocode-custom-component-gps-to-street-address/22233).
- [**sensor/shabbat_times**](config/custom_components/sensor/shabbat_times.py) made by myself, you can have a look [here](https://community.home-assistant.io/t/get-shabbat-times-from-hebcal-api-custom-sensor/32429).
- [**media_player/broadlink**](config/custom_components/media_player/broadlink.py) as instructed in [this post](https://community.home-assistant.io/t/broadlink-ir-media-player-for-old-dump-tvs/27706). The files in the [*config/ir_codes*](config/ir_codes) folder are relates to this component.

#### Python Scripts
 - [**service_call_loop.py**](config/python_scripts/service_call_loop.py) a simple python script I made for performing the same service call multiple times.
 
### Themes
- None of the [themes](config/themes) were made by myself, I'm not a frontend man. All of the themes I use are downloaded from the [Share your Themes forum](https://community.home-assistant.io/t/share-your-themes/22018).

### Installed Hass.io Addons
- [**Bluthooth BCM43xx**](https://home-assistant.io/addons/bluetooth_bcm43xx/) for use of the bluetooth device tracker.
- [**DuckDNS**](https://home-assistant.io/addons/duckdns/) to update DuckDNS servers with my modem's ip address, the addon also uses the [Let's Encrypt Addon](https://home-assistant.io/addons/lets_encrypt/) for an ssl certificate.
- [**SSH Server**](https://home-assistant.io/addons/ssh/) for accessing the system with putty.
- [**Samba Share**](https://home-assistant.io/addons/samba/) for accessing my configuration files from a windows environment.
- [**Mosquitto MQTT Broker**](https://home-assistant.io/addons/mosquitto/) for mqtt connectivity with home assistant, owntracks and my computer's local client.

### Frontend
First of all, I want to acknowledge the theme I use, one of the best themes I saw for home assistant. Needles to say, it isn't my creation, I don't (and won't) do frontend. The theme is called *Solarized* and I got it [here](https://community.home-assistant.io/t/share-your-themes/22018/31).
I'll now cover the views I've created in my home assistant installation:
- [HOME](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_HOME.jpg), this is my most used view. I use it to control the basic overall controls of home assistant:
  - **Shabbat Times Group** for getting the next or current shabbat start and end date and time for a couple of predefined cities.
  - **Manage Automations** for turning on or off specific automations.
  - **Start Scenes** for activating the light scenes.
  - **Activate Operations** for activating specific scripts.
  - **Household** gathering location and battery data for the household members. The location sensor is a bit complexed, its value is based on 3 diffrent trackers and a couple of geocode sensors. It will either show the zone (if in a known zone) or the address I'm in.</br>
  Another cool thing in this panel, the batery level icon changes accoarding to the battery level and rather or it's currently connected to the charger.
  - **Door Sensors** for tracking my door sensors.
  - **Spotify** for controlling my spotify account.
- [LIVING ROOM](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_LIVING_ROOM.jpg)
  - **Sensors** nothing special here, just a grouping of my living room sensors.
  - **Main AC** I really like this panel, it a has alot of scripts and automations surrounding it, it works very much like the regulat IR remote.
  - **TV Led** also a great panel, controlling my lifx-z led strip behind the tv.
  - **Lights** nothing special here, just a grouping of my living room lights.
-[KITCHEN](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_KITCHEN.jpg), nothing special here, just lights and sensors.
-[BATHROOMS](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_BATHROOMS.jpg), nothing special here, just lights and sensors.
-[HALLWAYS](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_HALLWAYS.jpg), nothing special here, just lights.
-[SERVICE ROOM](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_SERVICE_ROOM.jpg), nothing special here, just lights and sensors.
- [BEDROOM](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_BEDROOM_AC_OFF.jpg), besides the regular lights and sensors panels, I also have the **Bedroom AC** panel which is a bit different from the AC panel in the living. I has a hidden group that will only show when the ac is on, I've called it *Extra Controls* and [this](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_BEDROOM_AC_ON.jpg) is what it looks like when the ac is on, [this](https://github.com/TomerFi/my_home_assistant_configuration/blob/master/frontend_pics/View_BEDROOM_AC_EXTRA.jpg) is what it looks like when I open it.

## Network Gear
- [**TP-Ling C7 AC1750**](https://www.amazon.com/TP-Link-Archer-C7-802-11ac-Wireless/dp/B00BUSDVBQ/ref=sr_1_4?ie=UTF8&qid=1510661698&sr=8-4&keywords=tp-link+ac1750) is my main router, this is my lan, it connects to my modem and to all the endpoint via hubs, access points or direct connections.
- **3X** [**Google Wifi Points**](https://www.amazon.com/gp/product/B01MAW2294/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1) spreaded as wifi access points, I'm not using the mesh network functionality becouse it's not supported in ap mode. But I did named all the ssid the same, and the handoff between them are great so I actually have one wifi network through out my house.
- [**Netgear Prosafe 5 ports hub**](https://www.amazon.com/gp/product/B00HGLVZLY/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1).
- [**Edimax 5 ports hub**](https://www.amazon.com/Edimax-ES-5500GV3-Gigabit-Ethernet-Switch/dp/B00H8XIZT0/ref=sr_1_12?s=electronics&ie=UTF8&qid=1510662309&sr=1-12&keywords=edimax+switch).
- **4X Netowrk RJ45 to Coax Convertors** I've received from my cable supllier *Yes*, I used them to get the wired connectivity to different areas in my house.

## Smart Home Devices, Equipment and Endpoints
- [**Home Assistant Hass.io**](https://home-assistant.io/hassio/) installed on a [raspberry pi 3](https://www.amazon.com/gp/product/B01C6EQNNK/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1).
- **Windows MQTT Client** wriiten in java by myself, with a controller for activating windows applications based on recived payloads. You can have a look [here](https://community.home-assistant.io/t/how-i-made-alexa-talk-to-my-computer-through-home-assistant/32448).
- **5X** [**Amazon Alexa Enabled Devices**](https://www.amazon.com/Amazon-Echo-And-Alexa-Devices/b/ref=nav_shopall_1_ods_ha_echo_cp?ie=UTF8&node=9818047011), 2X Echo 1st generation (1 in the living room and 1 in the bedroom), 2X Echo Dot 2nd generation (1 in the den and 1 in the car), 1X Dash Wans laying around the house.
- [**Lifx-Z 2 meters led strip**](https://www.amazon.com/gp/product/B01KY02NLY/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) behind the living room's television.
- [**Harmony Elite**](https://www.amazon.com/gp/product/B014PDFP9S/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1) in the living room controling the following devices:
  - Samsung Smart TV
  - Yes STB
  - [Nvidia Shield Console](https://www.amazon.com/gp/product/B01N1NT9Y6/ref=oh_aui_detailpage_o02_s00?ie=UTF8&th=1).
  - [Harman Kardon Sabre SB35](https://www.amazon.com/Harman-Kardon-SABRE-SB35-Entertainment/dp/B00F9HTX7U/ref=sr_1_1?s=electronics&ie=UTF8&qid=1510609535&sr=1-1&keywords=sabre+sb35).
  - [Lifx-Z led strip](https://www.amazon.com/gp/product/B01KY02NLY/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1).
- [**Broadlink RM Pro**](https://www.aliexpress.com/item/Broadlink-RM2-RM-Pro-Smart-home-Automation-Universal-Intelligent-wireless-remote-control-WIFI-IR-RF-switch/32738344424.html?spm=a2g0s.9042311.0.0.elfcCR) in the living room controling the following devices:
  - Electra Classic 35 Air Conditioner in the living room.
  - 8X [Broadlink TC2 1Gang Switches EU Standart](https://www.aliexpress.com/item/2016-New-Arrival-Broadlink-TC2-Light-Touch-Switch-EU-220V-1Gang-Wall-Switch-White-Touch-Panel/32592935925.html?spm=a2g0s.9042311.0.0.elfcCR).
  - 2X [Broadlink TC2 2Gang Switches EU Standart](https://www.aliexpress.com/item/2016-New-Arrival-Broadlink-TC2-Touch-Switches-2Gang-EU-220V-Remote-Control-Wall-Light-Switch-Smart/32592959665.html?spm=a2g0s.9042311.0.0.elfcCR).
  - [Broadlink TC2 3Gang Switch US Standart](https://www.aliexpress.com/item/2016-New-Broadlink-TC2-Light-Touch-Switch-US-AU-110V-3Gang-Wall-Switch-Wireless-Remote-Control/32591265614.html?spm=a2g0s.9042311.0.0.1rwADH).
- **2X** [**Broadlink SP2 Plugs**](https://www.aliexpress.com/item/Broadlink-16A-EU-US-wifi-power-socket-SP-CC-Home-Automation-Smart-plug-outlet-Wireless-Control/32639393902.html?spm=a2g0s.9042311.0.0.1rwADH) for a night lamp in the living room and a simple led strip in the kitchen.
- [**Broadlink SC1 Outer Plug**](https://www.aliexpress.com/item/New-Broadlink-SC1-Wifi-Smart-Remote-Controlled-Power-Home-Automation-APP-Wireless-power-light-Switch-Via/32811421862.html?spm=a2g0s.9042311.0.0.1rwADH) for my service room light.
- [**Broadlink RM Mini**](https://www.aliexpress.com/item/Original-Broadlink-RM-Mini3Black-bean-Smart-Home-Automation-Universal-Intelligent-WiFi-IR-4G-Wireless-Controller-by/32657100947.html?spm=a2g0s.9042311.0.0.1rwADH) controlling the following devices:
  - Hisense Simple IR TV
  - Yes STB
  - Elco Air Conditioner
- [**Broadlink S1c 1st generation Alarm Kit**](https://www.aliexpress.com/item/2015-New-Arrival-Broadlink-S1-S1C-SmartOne-Alarm-Security-Kit-For-Home-Smart-Home-Alarm-System/32523639274.html?spm=a2g0s.9042311.0.0.1rwADH) working with 4X [Broadlink magnetic sensors](https://www.aliexpress.com/item/Original-Broadlink-S1C-433Mhz-Door-Sensor-Contact-Wireless-Window-Magnet-Entry-Detector-Sensor-Smart-Home-Alarm/32694362268.html?spm=a2g0s.9042311.0.0.8GFN5e).
- [**Broadlink A1 Sensor**](https://www.aliexpress.com/item/Broadlink-A1-E-air-wifi-Air-Quatily-Detector-Intelligent-Purifier-smart-home-Automation-phone-detect-Temperature/32614430027.html?spm=a2g0s.9042311.0.0.6NtFMx).

## Alexa Skills Configuration
- Store Skills:
  - [Broadlink Remote Control](https://www.amazon.com/BroadLink-Remote-Control/dp/B073PLQYKS/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1510648170&sr=1-1&keywords=broadlink) for controlling the tv in the bedroom.
  - [Harmony](https://www.amazon.com/Logitech-Harmony/dp/B01M4LDPX3/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1510648428&sr=1-1&keywords=harmony) for controlling the entertainment center in the living room.
  - [LIFX Optimized for Smart Home](https://www.amazon.com/LIFX-Optimized-for-Smart-Home/dp/B01EIQSPOY/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1510648575&sr=1-1&keywords=lifx) for controling my led strip.
  - [Shabbat Times](https://www.amazon.com/Tomer-Figenblat-Shabbat-Times/dp/B072PRCHRD/ref=sr_1_2?s=digital-skills&ie=UTF8&qid=1510648624&sr=1-2&keywords=shabbat+times) for getting the start and end times for the shabbat.
- Personal Skills:
  - [Ask My Pc](alexa_skills/ask_my_pc) the skill https endpoint is my home assistant installation, I use this skill to publish payloads to my computer through home assistant, you can have a look [here](https://www.youtube.com/watch?v=AQzD0TPG-xE).</br>
  The invocation name I use for this skil is *computer*, the phrase I use to invoke it is *Alexa, ask computer*.
  - [Home Assistant](alexa_skills/home_assistant) for controling my home assistant installation, I use it to run scripts, receive reports and retrieve data.</br>
  The invocation name I use for this skil is *home*, the phrase I use to invoke it is *Alexa, ask home*.
- Core Functionality
  - My Home Assistant installation acts as an  [Emulated Hue](https://home-assistant.io/components/emulated_hue/) platform making devices discoverable from alexa as Hue Lights. I use the emulated hue component from controlling most of my switches and all of my scenes.

## Useful Tools and Applications
- [**Notepad++**](https://notepad-plus-plus.org/) I use it for editing *YAML* and *JSON* files.
- [**Sublime Text**](https://www.sublimetext.com/) I use if for writing and editing *JavaScript* and *Python* scripts.
- [**Eclipse**](https://www.eclipse.org/) for *Java* developing.
- [**JSONLint**](https://jsonlint.com/) a very easy and simple *JSON* validator.
- [**JSLint**](http://www.jslint.com/) one of the best *JavaScript* validator I ran into.
- [**PEP8**](http://pep8online.com/) a very easy and simple *Python* validator.
- [**Python Command Line**](https://www.python.org/) built into the python installer, I use it to test *Python* code.
- [**Putty**](http://www.putty.org/) the most usefull ssh client I know.
- [**Postman**](https://www.getpostman.com/) a very useful tool for posting http rest requests.

I also want to acknowledge a couple of builtin tools with home assistant that I use regularly. in the developer tools:
- **Services** a very useful tool for testing service calls before integrating them into my yaml files.
- **Templates** there is no way I'm even looking at a template in the yaml files without testing it with this tool first, amazing.
