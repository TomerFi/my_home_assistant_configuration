# My  Home Assistant Configuration
This is my home assistant configruation, although I'm going to focus mainly on home assistant, I'll also talk about my smart home devices and my digital assistants configuration in order to fully describe my smart home.</br>
I will try to keep this repository updated with any changes I'll make in my working environment as much as I can.

**Environment**
- Installation: [Home Assistant in a Python virtual environment](https://www.home-assistant.io/docs/installation/virtualenv/)
- Current Installed Version: 0.84.6
- Platform: Raspberry Pi 3 B

**Table Of Contents**
- [Home Assistant](#home-assistant)
  - [Custom Components](#custom-components)
  - [Custom UI](#custom-ui)
  - [Python Scripts](#python-scripts)
- [Network Gear](#network-gear)
- [Smart Home Devices, Equipment and Endpoints](#smart-home-devices-equipment-and-endpoints)
  - [DIY Projects](#diy-projects)
- [AppDaemon](#appdaemon)
  - [Dashboards](#dashboards)
  - [Apps](#apps)
- [Alexa Skills Configuration](#alexa-skills-configuration)
- [Google Action Configuration](#google-action-configuration)

## Home Assistant

### Custom Components
- [**date_notifier**](custom_components/date_notifier.py) made by myself, get it [here](https://github.com/TomerFi/home-assistant-custom-components/tree/master/date_notifier).
- **sensor/google_geocode** as instructed in [this post](https://community.home-assistant.io/t/google-geocode-custom-component-gps-to-street-address/22233).
- [**sensor/shabbat_times**](custom_components/sensor/shabbat_times.py) made by myself, you can get it [here](https://github.com/TomerFi/home-assistant-custom-components/tree/master/shabbat_times).
- **media_player/broadlink** as instructed in [this post](https://community.home-assistant.io/t/broadlink-ir-media-player-for-old-dump-tvs/27706). The files in the [*ir_codes*](ir_codes) folder are related to this component.
- [**switcher_aio**](custom_components/switcher_aio) made by myself, you can get it [here](https://github.com/TomerFi/home-assistant-custom-components/tree/master/switcher_aio).
- [**sensor/broadlink_s1c**](custom_components/sensor/broadlink_s1c.py). made by myself, you can get it [here](https://github.com/TomerFi/home-assistant-custom-components/tree/master/broadlink_s1c).
- [**smartthings_bridge**](custom_components/smartthings_bridge) as the bridge component and [**sensor/smartthings_bridge**](custom_components/sensor/smartthings_bridge.py) as the sensor entity. made by myself, you can get it [here](https://github.com/TomerFi/home_assistant_smartthings_bridge).

### Custom UI
 - [**Script with Custom Text**](www/custom_ui/state-card-script-custom-text.html) made by myself for change the "ACTIVATE" value of the script entities, you can get it [here](https://github.com/TomerFi/home-assistant-custom-ui#script-with-custom-text).
 - **Custom UI: Tiles** as instructed in [this post](https://community.home-assistant.io/t/custom-ui-tiles/29513).

### Python Scripts
 - [**set_entity_state.py**](python_scripts/set_entity_state.py) a simple python script I made for changing entities states without launchin a state change event, meaning the state will change but no action will occur.
 - [**service_call_loop.py**](python_scripts/service_call_loop.py) a simple python script I made for performing the same service call multiple times.

## Network Gear
- **Vrtech IAD604** this is my main router and modem supllied by my ISP.
- **3X** [**Google Wifi Points**](https://www.amazon.com/gp/product/B01MAW2294/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1) spreaded as wifi access points, I'm not using the mesh network functionality becouse it's not supported in ap mode. But I did named all the ssid the same, and the handoff between them are great so I actually have one wifi network through out my house.
- [**Netgear Prosafe 5 ports hub**](https://www.amazon.com/gp/product/B00HGLVZLY/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1).
- [**Netgear 8 ports hub**](https://www.amazon.com/gp/product/B00KFD0SEA/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1).
- [**Edimax 5 ports hub**](https://www.amazon.com/Edimax-ES-5500GV3-Gigabit-Ethernet-Switch/dp/B00H8XIZT0/ref=sr_1_12?s=electronics&ie=UTF8&qid=1510662309&sr=1-12&keywords=edimax+switch).
- **4X Netowrk RJ45 to Coax Convertors** I've received from my cable supllier *Yes*, I used them to get the wired connectivity to different areas in my house.

## Smart Home Devices, Equipment and Endpoints
- [**Home Assistant**](https://www.home-assistant.io/docs/installation/virtualenv/) installed on a [raspberry pi 3 b](https://www.amazon.com/gp/product/B01C6EQNNK/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1) hosting the following services:
  - MYSQL database server for hosting Home Assistant's data.
  - AppDaemon for running python apps with home assistant (AppDaemon deserves its own [section](#appdaemon)).
- **Home Server** my home server is an installation of [RASPBIAN STRETCH LITE](https://www.raspberrypi.org/downloads/raspbian/) installed on a [raspberry pi 3 b+](https://www.amazon.com/gp/product/B07BC6WH7V/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) hosting the following services:
  - NGINX as a reverse proxy.
  - CERTBOT for managing my [Let's Encrypt](https://letsencrypt.org/) certificates.
  - MOSQUITTO MQTT for passing payloads from my various services and devices to home assistant.
  - DNSMASQ as a dns and dhcp servers.
- **Windows MQTT Client** written in java by myself, with a controller for activating windows applications based on received payloads. You can have a look [here](https://community.home-assistant.io/t/how-i-made-alexa-talk-to-my-computer-through-home-assistant/32448), see the client in action [here](https://www.youtube.com/watch?v=AQzD0TPG-xE) and get the instructions for how to use it [here](https://github.com/TomerFi/smathhome_computer_mqtt_client).
- **6X** [**Amazon Alexa Enabled Devices**](https://www.amazon.com/Amazon-Echo-And-Alexa-Devices/b/ref=nav_shopall_1_ods_ha_echo_cp?ie=UTF8&node=9818047011), 2X Echo 1st generation (1 in the kitchen and 1 in the bedroom), 2X Echo Dot 2nd generation (1 in the den and 1 in the living room), 1X Echo Dot 3rd generation in the nursery and 1X Dash Wand laying around the house.
- [**Google Home Mini**](https://store.google.com/us/product/google_home_mini?hl=en-US) in my office.
- [**Google Chromecast**](https://store.google.com/us/product/chromecast_2015?hl=en-US) connected to a Metz TV in my office.
- **Xbox 360** connected to a Metz TV in my office.
- [**Amcrest 2K Wireless IP Camera 3MP**](https://www.amazon.com/gp/product/B01LWK9VFS/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1) as a security/nursery video monitor using [Qnap's QVR Pro App](https://www.qnap.com/solution/qvr-pro-official/en/) running on my [Qnap TS-251A](https://www.amazon.de/gp/product/B01K6TWQD8/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1).
- [**Lifx-Z 2 meters led strip**](https://www.amazon.com/gp/product/B01KY02NLY/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) behind the living room's television.
- [**Philips Hue Smart Hub**](https://www.amazon.com/gp/product/B016H0QZ7I/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1) controlling the following:
  - [Philips Hue Smart Dimmer Switch](https://www.amazon.com/dp/B076MGKTGS/ref=sxbs_sxwds-stppvp_1?pf_rd_p=d45777d6-4c64-4117-8332-1659db52e64f&pd_rd_wg=4d9JG&pf_rd_r=PDBMWEWMRVBNEN8K2ETK&pd_rd_i=B076MGKTGS&pd_rd_w=npz5i&pd_rd_r=8721dbcb-d164-4c7d-aeff-40fcf0140caf&ie=UTF8&qid=1546435068&sr=1) controlling the nursery ceiling light.
  - 3X [Philips Hue White Ambiance Bulb](https://www.amazon.com/gp/product/B01F6T4R0S/ref=oh_aui_detailpage_o08_s00?ie=UTF8&th=1) two in the nursery's ceiling light and one in the living room night light.
  - [Philips Hue White and Color Ambiance LightStrip Plus](https://www.amazon.com/gp/product/B0167H33DU/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1) behind the dresser in the nursery.
  - [Philips Hue Bloom](https://www.amazon.com/gp/product/B07BNRYGYX/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1) behind the feeding chair in the nursery.
- **2X** [**Fire HD 8 Tablet**](https://www.amazon.com/gp/product/B0794RHPZD/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1) one mounted on the nursery wall running [WallPanel](https://github.com/WallPanel-Project/wallpanel-android) to display an [AppDaemon Dashboard](#dashboards), and the other sits on the kitchen's island connected to a [Show Mode Charging Dock](https://www.amazon.com/dp/B07FQVQZKN/ref=fs_ods_tab_zskar).
- [**SmartThings Link for Nvidia Shield**](https://www.amazon.com/gp/product/B071GSVP6Z/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1) connected to my [Nvidia Shield](https://www.amazon.com/gp/product/B01N1NT9Y6/ref=oh_aui_detailpage_o06_s00?ie=UTF8&psc=1) amd used as a [SmartThings Hub](https://www.smartthings.com/).
- [**Harmony Elite**](https://www.amazon.com/gp/product/B014PDFP9S/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1) in the living room controlling the following devices:
  - Samsung Smart TV
  - Yes STB
  - [Nvidia Shield Console](https://www.amazon.com/gp/product/B01N1NT9Y6/ref=oh_aui_detailpage_o02_s00?ie=UTF8&th=1).
  - [Harman Kardon Sabre SB35](https://www.amazon.com/Harman-Kardon-SABRE-SB35-Entertainment/dp/B00F9HTX7U/ref=sr_1_1?s=electronics&ie=UTF8&qid=1510609535&sr=1-1&keywords=sabre+sb35).
  - [Lifx-Z led strip](https://www.amazon.com/gp/product/B01KY02NLY/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1).
- [**Broadlink RM Pro**](https://www.aliexpress.com/item/Broadlink-RM2-RM-Pro-Smart-home-Automation-Universal-Intelligent-wireless-remote-control-WIFI-IR-RF-switch/32738344424.html?spm=a2g0s.9042311.0.0.elfcCR) in the living room controlling the following devices:
  - Electra Classic 35 Air Conditioner in the living room.
  - 8X [Broadlink TC2 1Gang Switches EU Standart](https://www.aliexpress.com/item/2016-New-Arrival-Broadlink-TC2-Light-Touch-Switch-EU-220V-1Gang-Wall-Switch-White-Touch-Panel/32592935925.html?spm=a2g0s.9042311.0.0.elfcCR).
  - 2X [Broadlink TC2 2Gang Switches EU Standart](https://www.aliexpress.com/item/2016-New-Arrival-Broadlink-TC2-Touch-Switches-2Gang-EU-220V-Remote-Control-Wall-Light-Switch-Smart/32592959665.html?spm=a2g0s.9042311.0.0.elfcCR).
  - [Broadlink TC2 3Gang Switch US Standart](https://www.aliexpress.com/item/2016-New-Broadlink-TC2-Light-Touch-Switch-US-AU-110V-3Gang-Wall-Switch-Wireless-Remote-Control/32591265614.html?spm=a2g0s.9042311.0.0.1rwADH).
- [**Broadlink SP2 Plug**](https://www.aliexpress.com/item/Broadlink-16A-EU-US-wifi-power-socket-SP-CC-Home-Automation-Smart-plug-outlet-Wireless-Control/32639393902.html?spm=a2g0s.9042311.0.0.1rwADH) controlling a simple led strip in the kitchen.
- [**Broadlink SC1 Outer Plug**](https://www.aliexpress.com/item/New-Broadlink-SC1-Wifi-Smart-Remote-Controlled-Power-Home-Automation-APP-Wireless-power-light-Switch-Via/32811421862.html?spm=a2g0s.9042311.0.0.1rwADH) for my service room light.
- **3X** [**Broadlink RM Mini**](https://www.aliexpress.com/item/Original-Broadlink-RM-Mini3Black-bean-Smart-Home-Automation-Universal-Intelligent-WiFi-IR-4G-Wireless-Controller-by/32657100947.html?spm=a2g0s.9042311.0.0.1rwADH) controlling the following devices:
  - Hisense simple IR TV in the bedroom.
  - Yes STB in the bedroom.
  - Elco Air Conditioner in the bedroom.
  - Elco Air Conditioner in the nursery.
  - Metz simple IR TV in the office.
  - Hyundai Ceiling Fan in the office.
- [**Broadlink S1c 1st generation Alarm Kit**](https://www.aliexpress.com/item/2015-New-Arrival-Broadlink-S1-S1C-SmartOne-Alarm-Security-Kit-For-Home-Smart-Home-Alarm-System/32523639274.html?spm=a2g0s.9042311.0.0.1rwADH) working with 5X [Broadlink magnetic sensors](https://www.aliexpress.com/item/Original-Broadlink-S1C-433Mhz-Door-Sensor-Contact-Wireless-Window-Magnet-Entry-Detector-Sensor-Smart-Home-Alarm/32694362268.html?spm=a2g0s.9042311.0.0.8GFN5e), 1X [Broadlink PIR mostion sensor](https://www.aliexpress.com/item/Original-BroadLink-Smart-Home-Wireless-Intelligent-Infrared-PIR-Motion-Sensor-Anti-theft-for-Home-Security-S1/32757643751.html?spm=2114.search0104.3.8.3fc8a236izI5LU&ws_ab_test=searchweb0_0,searchweb201602_3_10065_10068_319_10059_10884_317_10887_10696_100031_321_322_10084_453_10083_454_10103_10618_10307_537_536,searchweb201603_51,ppcSwitch_0&algo_expid=126dccf7-f4b5-4a2b-b329-a0c6626a8846-1&algo_pvid=126dccf7-f4b5-4a2b-b329-a0c6626a8846) and 1X [Broadlink Key Fob remote control](https://www.aliexpress.com/item/Original-Broadlink-S1C-S1-S2-Key-Fob-Remote-Control-Activate-Select-Sensors-For-S1-S1C-SmartONE/32842170690.html?spm=2114.search0104.3.94.45e06ef7elLUke&ws_ab_test=searchweb0_0,searchweb201602_3_10065_10068_319_10059_10884_317_10887_10696_100031_321_322_10084_453_10083_454_10103_10618_10307_537_536,searchweb201603_51,ppcSwitch_0&algo_expid=5b984a39-8673-41e1-96b9-2a3d74a7c7df-14&algo_pvid=5b984a39-8673-41e1-96b9-2a3d74a7c7df).
- [**Broadlink A1 Sensor**](https://www.aliexpress.com/item/Broadlink-A1-E-air-wifi-Air-Quatily-Detector-Intelligent-Purifier-smart-home-Automation-phone-detect-Temperature/32614430027.html?spm=a2g0s.9042311.0.0.6NtFMx).
- [**Switcher V2 Boiler Switch**](https://www.switcher.co.il/%D7%9E%D7%95%D7%A6%D7%A8/%D7%A1%D7%95%D7%95%D7%99%D7%A6%D7%A8/?doing_wp_cron=1519315002.3308029174804687500000).
- [**RF Doorbell**](https://www.aliexpress.com/item/Plug-in-Wireless-Door-Bell-Waterproof-US-Plug-Push-Button-36-Chimes-1-Ourdoor-Transmitter-2/32326166816.html?spm=a2g0s.9042311.0.0.719e4c4dV4Xc1V).
- [**RF Remote 1Gang**](https://www.aliexpress.com/item/VHOME-EU-UK-Smart-Home-433MHZ-RF-Smart-Remote-Control-transmitter-220V-Crystal-Panel-Touch-Wall/32755499771.html?spm=a2g0s.9042311.0.0.27424c4dKhoqUz).
- [**RF Remote 2Gang**](https://www.aliexpress.com/item/Vhome-Smart-home-Wireless-433MHz-Wall-stickers-Remote-Control-transmitter-with-EU-UK-2gang-1-Way/32742594094.html?spm=a2g0s.9042311.0.0.27424c4dKhoqUz)

### DIY Projects
- [**ESP-MQTT-JSON-Multisensor**](https://github.com/bruhautomation/ESP-MQTT-JSON-Multisensor) Amazing and Simple. The DIY multi-sensor by the one and only BRUH. I've made only one so far, I use it in my office.
- [**OpenMqttGateway**](https://github.com/1technophile/OpenMQTTGateway) A Perfect Project. RF >> MQTT, MQTT >> RF. I use this project to capture a RF packets from various remotes (and a doorbell) and and pass them to HA as mqtt topics.

## AppDaemon
*under construction*

### Dashboards
*under construction*

### Apps
*under construction*

## Alexa Skills Configuration
*under construction*

## Google Action Configuration
*under construction*
