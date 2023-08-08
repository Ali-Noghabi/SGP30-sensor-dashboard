#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include "Adafruit_SGP30.h"

const char* ssid = "Ali";
const char* password = "Ali123ali";
const char* host = "192.168.1.160";
const int port = 5000;

WebSocketsClient webSocket;
Adafruit_SGP30 sgp;

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }  // Wait for serial console to open!

  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("-");
  }
  Serial.println();
  Serial.print("WiFi connected, IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to WebSocket server
  webSocket.begin(host, port, "/", "");
  webSocket.onEvent(webSocketEvent);

  //connect to spg sensor
  if (!sgp.begin()) {
    Serial.println("Sensor not found :(");
    while (1)
      ;
  }
  Serial.print("Found SGP30 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);
}

void loop() {

  //get data from sensor and send it to server every 1 secound

  if (millis() % 1000 == 0) {
    if (!sgp.IAQmeasure()) {
      Serial.println("Measurement failed");
      return;
    }
    Serial.print("TVOC ");
    Serial.print(sgp.TVOC);
    Serial.print(" ppb\t");
    Serial.print("eCO2 ");
    Serial.print(sgp.eCO2);
    Serial.println(" ppm");

    if (!sgp.IAQmeasureRaw()) {
      Serial.println("Raw Measurement failed");
      return;
    }
    Serial.print("Raw H2 ");
    Serial.print(sgp.rawH2);
    Serial.print(" \t");
    Serial.print("Raw Ethanol ");
    Serial.print(sgp.rawEthanol);
    Serial.println("");

    int tvoc = sgp.TVOC;  // Replace with your TVOC value
    int eco2 = sgp.eCO2;  // Replace with your eCO2 value
    int rawh2 = sgp.rawH2;  // Replace with your eCO2 value
    int rawethanol = sgp.rawEthanol;  // Replace with your eCO2 value

    StaticJsonDocument<200> doc;
    doc["TVOC"] = tvoc;
    doc["eCO2"] = eco2;
    doc["rawH2"] = rawh2;
    doc["rawEthanol"] = rawethanol;
    String message;
    serializeJson(doc, message);
    webSocket.sendTXT(message);
  }

  // Handle WebSocket events
  webSocket.loop();
}

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("Disconnected from server");
      break;
    case WStype_CONNECTED:
      Serial.println("Connected to server");
      break;
    case WStype_TEXT:
      Serial.printf("Received message: %.*s\n", length, payload);
      break;
    default:
      break;
  }
}