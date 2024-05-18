# aqualogic

Forked from https://github.com/swilson/aqualogic.  This fork uses a script on a EW11 to handle the timing of the fram sends locally instead of over the network.

- Removed keep_alive and retry code.  This is done on a script on the EW11.
  - Script from https://www.troublefreepool.com/threads/aql-ps-8-remote-emulator-app.244915/
- Added unique_id to switches and sensors so that they can be edited in the HA UI.
- Added service, menu, up, down, plus, minus switches.
- Added display sensor.
- Migrated in code from other forks (heater stuff is untested in this fork).
- Added more error handling.
- Commented out web server code.
- Other small tweaks.
- This fork is for a P4, but you can change to a P8 in the core.py. Look at get_key_event_frame(). 
----
A python library to interface with Hayward/Goldline AquaLogic/ProLogic pool controllers. Based on Goldline prototol decoding work done by draythomp (http://www.desert-home.com/p/swimming-pool.html). Used by the [Home Assistant AquaLogic component](https://www.home-assistant.io/components/aqualogic/).

Since the Goldline protocol uses RS-485, a hardware interface is required. I'm using an [RS-485 to Ethernet adapter](https://www.usriot.com/products/rs485-to-ethernet-converter.html), though you could use some other type of adapter (e.g. RS-485 to RS-232); the library supports both socket and serial connections.

In addition to the API, the library also provides a rudimentary web interface. This allows the user to cycle through the menu system to perform manual tasks such as setting the heater temperature.

- [RS-485 Notes](https://github.com/swilson/aqualogic/wiki/RS%E2%80%90485-Notes)
- [TriStar VS Pump Notes](https://github.com/swilson/aqualogic/wiki/TriStar-VS-Pump-Notes)
- [Upgrading the AquaLogic Firmware](https://github.com/swilson/aqualogic/wiki/Upgrading-the-AquaLogic-Firmware)
- [Wired Remote Repair](https://github.com/swilson/aqualogic/wiki/Wired-Remote-Repair)

Tested on an AquaLogic P4 with Main Software Revision 2.91. YMMV.

This project is not affiliated with or endorsed by Hayward Industries Inc. in any way. 
