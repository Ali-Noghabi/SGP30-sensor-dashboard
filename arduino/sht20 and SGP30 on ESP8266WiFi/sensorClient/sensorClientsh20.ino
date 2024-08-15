#include <ESP8266WiFi.h>

#include <WebSocketsClient.h>

#include <ArduinoJson.h>

#include <Wire.h>

#include "Adafruit_SGP30.h"
#include "DFRobot_SHT20.h"

//server
const char * ssid = "Datall-2";
const char * password = "z1x2c3v4b5n6m0";
const char * host = "192.168.2.153"; //your server ip
const int port = 5000; //serverPort

//status
const int connectionStatus_PIN = 12;
const int isReceving_PIN = 14;
const int threshold_PIN = 13;

//thresholds
const int tvoc_threshold = 5000;
const int co2_threshold = 5000;
const int rawh2_threshold = 18000;
const int ethanol_threshold = 22000;
const int temperature_threshold = 50;
const int humidity_threshold = 100;

WebSocketsClient webSocket;
Adafruit_SGP30 sgp;
const int soil_moisture_pin = A0;
DFRobot_SHT20 sht20(&Wire, SHT20_I2C_ADDR);

void printRawDate(int tvoc, int eco2, int rawh2, int rawethanol, float temperature, float humidity, bool show_threshold);

void setup() {
  pinMode(connectionStatus_PIN, OUTPUT);
  pinMode(isReceving_PIN, OUTPUT);
  pinMode(threshold_PIN, OUTPUT);
  pinMode(soil_moisture_pin, INPUT);

  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  } // Wait for serial console to open!

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
    Serial.println("SGP Sensor not found :(");
    while (1)
    ;
  }

  sht20.initSHT20();
  delay(100);
  Serial.println("Sensor init finish!");
}

void loop() {

  //get raw data from sensor and send it to server every 10 secound

  if (millis() % 10000 == 0) {

    if (!sgp.IAQmeasure()) {
      Serial.println("Measurement failed");
      return;
    }
    int tvoc = sgp.TVOC; // Replace with your TVOC value
    int eco2 = sgp.eCO2; // Replace with your eCO2 value

    if (!sgp.IAQmeasureRaw()) {
      Serial.println("Raw Measurement failed");
      return;
    }
    int rawh2 = sgp.rawH2; // Replace with your eCO2 value
    int rawethanol = sgp.rawEthanol; // Replace with your eCO2 value

    float temperature =sht20.readHumidity();
    float humidity = sht20.readTemperature();
    // float temperature = 20;
    // float humidity = 31;

    int sensorValue = analogRead(soil_moisture_pin);
    Serial.print("Soil Moisture: ");
    Serial.println(sensorValue);

    if (tvoc < tvoc_threshold &&
      eco2 < co2_threshold &&
      rawh2 < rawh2_threshold &&
      rawethanol < ethanol_threshold &&
      temperature < temperature_threshold &&
      humidity < humidity_threshold) 
    {
      StaticJsonDocument < 200 > doc;
      doc["name"] = "sensor2";
      doc["TVOC"] = tvoc;
      doc["eCO2"] = eco2;
      doc["rawH2"] = rawh2;
      doc["rawEthanol"] = rawethanol;
      doc["Temperature"] = temperature;
      doc["Humidity"] = humidity;
      String message;
      serializeJson(doc, message);
      webSocket.sendTXT(message);
      digitalWrite(threshold_PIN, LOW);
      Serial.println("inside threshold zone");
      printRawDate(tvoc, eco2, rawh2, rawethanol, temperature, humidity , false);
    } else {
      Serial.println("inside critical zone!!");
      printRawDate(tvoc, eco2, rawh2, rawethanol, temperature, humidity ,true);
      digitalWrite(threshold_PIN, HIGH);
    }
  }

  // Handle WebSocket events
  webSocket.loop();
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
  case WStype_DISCONNECTED:
    digitalWrite(connectionStatus_PIN, LOW);
    Serial.println("Disconnected from server");
    break;
  case WStype_CONNECTED:
    digitalWrite(connectionStatus_PIN, HIGH);
    Serial.println("Connected to server");
    break;
  case WStype_TEXT:
    Serial.printf("Received message: %.*s\n", length, payload);
    digitalWrite(isReceving_PIN, HIGH);
    delay(10);
    digitalWrite(isReceving_PIN, LOW);
    break;
  default:
    break;
  }
}

void printRawDate(int tvoc, int eco2, int rawh2, int rawethanol, float temperature, float humidity, bool show_threshold) {
  if (show_threshold) {
    Serial.print("TVOC Threshold ");
    Serial.print(tvoc_threshold);
    Serial.print("\teCO2 Threshold ");
    Serial.print(co2_threshold);
    Serial.print("\nRawH2 Threshold ");
    Serial.print(rawh2_threshold);
    Serial.print("\tRawEthanol Threshold ");
    Serial.print(ethanol_threshold);
    Serial.print("\nTemperature Threshold ");
    Serial.print(temperature_threshold);
    Serial.print("\tHumidity Threshold \n");
    Serial.print(humidity_threshold);
  }
  Serial.print(tvoc);
  Serial.print(" ppb TVOC\t");
  Serial.print(eco2);
  Serial.println(" ppm eCO2");
  Serial.print(rawh2);
  Serial.print(" ppm RawH2\t");
  Serial.print(rawethanol);
  Serial.println(" ppm RawEthanol");
  Serial.print(temperature);
  Serial.print(" °C Temperature\t");
  Serial.print(humidity);
  Serial.println(" RH Humidity");
}