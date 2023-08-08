# SGP30 sensor dashboard using ESP8266 NodeMcu
- java script dashboard for SPG30 sensor using esp8266 nodemcu
- python server to save sensor data in database
  
# Setup
## Arduino

### install ide
-install arduino ide base on you OS
for manjaro
```
flatpak install cc.arduino.IDE2
```
### Install board package
-In your Arduino IDE, go to File> Preferences
-Enter http://arduino.esp8266.com/stable/package_esp8266com_index.json into the “Additional Boards Manager URLs” field as shown in the figure below. Then, click the “OK” button
-Open the Boards Manager. Go to Tools > Board > Boards Manager
-Search for ESP8266 and press install button for the “ESP8266 by ESP8266 Community“
-from Tools>Board>esp8266 chose NodeMCU 0.9 (or the board using)

### install library
In your Arduino IDE, go to Sketch> Include Library>Library manager
- Search for AVision_ESP8266 by A-Vision and install it with all linked libs
- Search for ArduinoJson by Benoit Blanchon and install it
- Search for Adafruit SGP30 Sensor by Adafruit and install it with all linked libs
