#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include "Adafruit_SGP30.h"
#include "DFRobot_SHT20.h"

const char* ssid = "wifiName";
const char* password = "wifiPassword";
const char* host = "serverIp";
const int port = 5000; //serverPort
const int connectionStatus_PIN = 12;
const int isReceving_PIN = 14;
WebSocketsClient webSocket;
Adafruit_SGP30 sgp;
DFRobot_SHT20 sht20(&Wire, SHT20_I2C_ADDR);
// LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  pinMode(connectionStatus_PIN, OUTPUT);
  pinMode(isReceving_PIN, OUTPUT);

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
    Serial.println("SGP Sensor not found :(");
    while (1)
      ;
  }

  sht20.initSHT20();
  delay(100);
  Serial.println("Sensor init finish!");

  // lcd.init();
  // // turn on LCD backlight                      
  // lcd.backlight();

}

void loop() {

  // //get data from sensor and send it to server every 1 secound
  // lcd.setCursor(0, 0);
  // // print message
  // lcd.print("Hello, World!");
  // delay(1000);
  // // clears the display to print new message
  // lcd.clear();
  // // set cursor to first column, second row
  // lcd.setCursor(0,1);
  // lcd.print("Hello, World!");
  // delay(1000);
  // lcd.clear();
  if (millis() % 3000 == 0) {


    if (!sgp.IAQmeasure()) {
      Serial.println("Measurement failed");
      return;
    }
    int tvoc = sgp.TVOC;  // Replace with your TVOC value
    int eco2 = sgp.eCO2;  // Replace with your eCO2 value
    Serial.print("TVOC ");
    Serial.print(tvoc);
    Serial.print(" ppb\t");
    Serial.print("eCO2 ");
    Serial.print(eco2);
    Serial.println(" ppm");

    if (!sgp.IAQmeasureRaw()) {
      Serial.println("Raw Measurement failed");
      return;
    }
    int rawh2 = sgp.rawH2;            // Replace with your eCO2 value
    int rawethanol = sgp.rawEthanol;  // Replace with your eCO2 value
    Serial.print("Raw H2 ");
    Serial.print(rawh2);
    Serial.print(" \t");
    Serial.print("Raw Ethanol ");
    Serial.print(rawethanol);
    Serial.println("");

    float temperature =sht20.readHumidity();
    float humidity = sht20.readTemperature();
    Serial.print("Temp: ");
    Serial.print(temperature);
    Serial.print(" C");
    Serial.print("\t\t");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" \% sensor2");

    StaticJsonDocument<200> doc;
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
  }

  // Handle WebSocket events
  webSocket.loop();
}

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      digitalWrite(connectionStatus_PIN, HIGH);
      Serial.println("Disconnected from server");
      break;
    case WStype_CONNECTED:
      digitalWrite(connectionStatus_PIN, LOW);
      Serial.println("Connected to server");
      break;
    case WStype_TEXT:
      Serial.printf("Received message: %.*s\n", length, payload);
      digitalWrite(isReceving_PIN, LOW);
      delay(10);
      digitalWrite(isReceving_PIN, HIGH);
      break;
    default:
      break;
  }
}