#include <ESP8266WiFi.h>
#include <Wire.h>
#include "Adafruit_SGP30.h"
#include "DFRobot_SHT20.h"

Adafruit_SGP30 sgp;
DFRobot_SHT20 sht20(&Wire, SHT20_I2C_ADDR);

void measureAirQuality();
void retrieveBaseline();

void setup() {

  Serial.begin(115200);
  while (!Serial) { delay(10); }  // Wait for serial console to open!

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

    float temperature = sht20.readHumidity();
    float humidity = sht20.readTemperature();
    Serial.print("Temp: ");
    Serial.print(temperature);
    Serial.print(" C");
    Serial.print("\t\t");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" \% sensor2");
  }
}

void calibrateSensor() {
  Serial.println("Starting sensor calibration...");

  // Expose the sensor to fresh air for 10 minutes for baseline calibration
  delay(10 * 60 * 1000);
  // Set baseline values using the current measurements
  sgp.setBaseline();
  // Mark calibration as complete and record the current time
  Serial.println("Sensor calibration complete.");
}

void measureAirQuality() {
  sgp.IAQmeasure();
  // Process and use the air quality data
}

void retrieveBaseline() {
  Serial.println("Retrieving baseline values...");

  // Retrieve baseline values
  uint16_t baselineTVOC, baselineCO2;
  if (sgp.getBaseline(&baselineCO2, &baselineTVOC)) {
    Serial.print("Baseline TVOC: ");
    Serial.print(baselineTVOC);
    Serial.print(" Baseline eCO2: ");
    Serial.println(baselineCO2);
  } else {
    Serial.println("Failed to retrieve baseline values.");
  }
}

void measureRawSignals() {
  Serial.println("Measuring raw signals...");

  // Measure raw signals
  if (sgp.IAQmeasureRaw()) {
    int rawH2 = sgp.rawH2;
    int rawEthanol = sgp.rawEthanol;
    
    Serial.print("Raw H2: ");
    Serial.print(rawH2);
    Serial.print("\t");
    Serial.print("Raw Ethanol: ");
    Serial.println(rawEthanol);
  } else {
    Serial.println("Failed to measure raw signals.");
  }
}
