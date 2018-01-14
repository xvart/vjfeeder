# vjfeeder

This is an MQTT backed interface to vJoy.

It uses MQTT to coordinate between devices where feedback is not present.


Get python3 for windows from here
https://www.activestate.com/activepython/downloads, use one of the python3x's

Get pyvjoy from
https://github.com/tidzo/pyvjoy

Install code for pyvjoy here C:\Python35\Lib\site-packages\pyvjoy

Get vjoy from http://vjoystick.sourceforge.net/site/
Libraries for your windows version AMD64 or x86 of vJoy need to be installed in the C:\Python35\Lib\site-packages\pyvjoy

Install hbmqtt on windows, in a terminal type "pip install hbmqtt"

pyfeeder.py will start the MQTT broker and listen to the broker to post to vJoy.

Connect to the broker at 1883 or websocket port 8883 and send it JSON packets.