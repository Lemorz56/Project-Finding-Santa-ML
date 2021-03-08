# Server scripts
This contains 2 files. The ino script for the ESP8266 and the python script to communicate with the server that runs on the ESP.

## ServerScript.py
At line 14 and 15 I'm specifying the locations of the certificates which you will not have. You need to create those by your own.
This python script creates a secure socket connection and waits. Once it gets called with true it goes to an url that makes a light on the ESP8266 turn on.

## WebServerPyth.ino
First of all you need to install the board config from Arduino.
Then put the WiFi Password inside a file called Password.h or create it. Then we have a simple server that turns a light on if an address gets an hit and another url that turns it off.