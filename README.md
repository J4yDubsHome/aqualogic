# AquaLogic

Forked from https://github.com/swilson/aqualogic.  This fork uses a script on a EW11 to handle the timing of the frame sends locally instead of over the network.

- Removed keep_alive and retry code (config option now).  This is done on a script on the EW11.
  - Script from https://www.troublefreepool.com/threads/aql-ps-8-remote-emulator-app.244915/
- Added unique_id to switches and sensors so that they can be edited in the HA UI.
- Added service, menu, up, down, plus, minus switches.
- Added display sensor.
- Migrated in code from other forks (heater stuff is untested in this fork).
- Added more error handling.
- Commented out web server code.
- Added config options for device, usescript, and p4p8.
- Renamed domain and directory so that it's seperate from the built-in AquaLogic intergration.
- Other small tweaks.
  
## Install
- If using a EW11, install the script on the device per the instructions at
  - https://docs.google.com/document/d/18dtxOf3cBQ9h4sAxC_g3rcm20pw5Xv7ds5K6pCOaUds/edit#heading=h.wg5enocutlte
- Download the files from this repository (Code > Download Zip)
- Place the aqualogic_p4p8 directory in config/custom_components/
- Modify your configuartion.YAML in config and add the below.  Other examples are in the "YAML Examples" directory (note I split the configuations into 3 files to keep configuration.YAML clean, this is a personal preference)
- Restart HA and look for the new entities that start with aqualogic

```
aqualogic_p4p8:
  host: 192.168.1.160   #Set to HostName, IP Address, or Serial path
  #host: /dev/ttyUSB0   #Serial example
  port: 4328            #Set port if using a network device
  device: socket        #Set to socket or serial
  usescript: True       #Set to False if not using script on a network device
  p4p8: p4              #Set to p4 or p8

sensor:
  - platform: aqualogic_ew11
    monitored_conditions:
      - pool_temp
      - <sensor list in "YAML Examples" directory>
switch:
  - platform: aqualogic_ew11
    monitored_conditions:
      - filter
      - <switch list in "YAML Examples" directory>
```
----
## Original readme
A python library to interface with Hayward/Goldline AquaLogic/ProLogic pool controllers. Based on Goldline prototol decoding work done by draythomp (http://www.desert-home.com/p/swimming-pool.html). Used by the [Home Assistant AquaLogic component](https://www.home-assistant.io/components/aqualogic/).

Since the Goldline protocol uses RS-485, a hardware interface is required. I'm using an [RS-485 to Ethernet adapter](https://www.usriot.com/products/rs485-to-ethernet-converter.html), though you could use some other type of adapter (e.g. RS-485 to RS-232); the library supports both socket and serial connections.

In addition to the API, the library also provides a rudimentary web interface. This allows the user to cycle through the menu system to perform manual tasks such as setting the heater temperature.

- [RS-485 Notes](https://github.com/swilson/aqualogic/wiki/RS%E2%80%90485-Notes)
- [TriStar VS Pump Notes](https://github.com/swilson/aqualogic/wiki/TriStar-VS-Pump-Notes)
- [Upgrading the AquaLogic Firmware](https://github.com/swilson/aqualogic/wiki/Upgrading-the-AquaLogic-Firmware)
- [Wired Remote Repair](https://github.com/swilson/aqualogic/wiki/Wired-Remote-Repair)

Tested on an AquaLogic P4 with Main Software Revision 2.91. YMMV.

This project is not affiliated with or endorsed by Hayward Industries Inc. in any way. 
