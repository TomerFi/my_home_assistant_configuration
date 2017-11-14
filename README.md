# My  Home Assistant Configuration
This is my home assistant configruation, although I'm going to focus on home assistat, I'll also talk about my smart home devices and my alexa configuration in order to fully scan my smart home.

**Table Of Contents**
- [Home Assistant](#home-assistant)
  - [Customization and modification](#customization-and-modification)
    - [Custom Addons](#custom-addons)
    - [Custom Components](#custom-components)
    - [Python Scripts](#python-scripts)
  - [Themes](#themes)
  - [Installed Hass.io Addons](#installed-hassio-addons)
- [Network Gear](#network-gear)
- [Smart Home Devices, Equipment and Endpoints](#smart-home-devices-equipment-and-endpoints)
- [Alexa Skills Configuration](#alexa-skills-configuration)

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

## Network Gear
- [**TP-Ling C7 AC1750**](https://www.amazon.com/TP-Link-Archer-C7-802-11ac-Wireless/dp/B00BUSDVBQ/ref=sr_1_4?ie=UTF8&qid=1510661698&sr=8-4&keywords=tp-link+ac1750) is my main router, this is my lan, it connects to my modem and to all the endpoint via hubs, access points or direct connections.
- **3X** [**Google Wifi Points**](https://www.amazon.com/gp/product/B01MAW2294/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1) spreaded as wifi access points, I'm not using the mesh network functionality becouse it's not supported in ap mode. But I did named all the ssid the same, and the handoff between them are great so I actually have one wifi network through out my house.
- [**Netgear Prosafe 5 ports hub**](https://www.amazon.com/gp/product/B00HGLVZLY/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1).
- [**Edimax 5 ports hub**](https://www.amazon.com/Edimax-ES-5500GV3-Gigabit-Ethernet-Switch/dp/B00H8XIZT0/ref=sr_1_12?s=electronics&ie=UTF8&qid=1510662309&sr=1-12&keywords=edimax+switch).
- **4X Netowrk RJ45 to Coax Convertors** I've received from my cable supllier *Yes*, I used them to get the wired connectivity to different areas in my house.

## Smart Home Devices, Equipment and Endpoints
- [**Home Assistant Hass.io**](https://home-assistant.io/hassio/) installed on a [raspberry pi 3](https://www.amazon.com/gp/product/B01C6EQNNK/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1).
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
  - AskMyPc home assistat skill controlling my computer.
  - Home Assistant for controling my home assistant installation.
- Core Functionality
  - My Home Assistant installation acts as an  [Emulated Hue](https://home-assistant.io/components/emulated_hue/) platform making devices discoverable from alexa as Hue Lights.
