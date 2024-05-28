# Fruit Ripening Monitoring System Using ESP8266 and VOC Sensors

## Overview

This project aims to monitor and analyze the relationship between various gases and fruit ripening. We use an ESP8266 NodeMCU microcontroller with SGP30, HTU21, and SHT20 sensors to gather data on VOC gases, CO2, H2, ethanol, temperature, and humidity. The collected data is sent to a Python server via WebSocket, which can handle multiple clients simultaneously. The data is stored in an SQLite database, cleaned, and prepared for future data mining to find correlations between the gases and fruit ripening.

![image](doc/readme/project-monitoring.png)
## Features

- **Real-time monitoring**: 
  - The system continuously collects data on VOC gases (including CO2, H2, ethanol) as well as temperature and humidity.
  - SGP30 sensor module captures the VOC gas concentrations.
  - HTU21 and SHT20 sensors measure the temperature and humidity respectively, ensuring precise environmental monitoring.

- **Multiple sensor modules**:
  - Multiple ESP8266 NodeMCU microcontrollers are used to gather data under different conditions to ensure a comprehensive and valid dataset.
  - Each microcontroller can independently collect data from its respective sensors and send it to the central server.

- **Data communication and storage**:
  - Data is transmitted from the ESP8266 microcontrollers to the Python server using WebSocket, ensuring real-time data transfer.
  - The Python server can handle multiple client connections at once, making it scalable for larger setups.
  - All collected data is stored in an SQLite database, providing a structured and efficient way to manage large volumes of data.

- **Data cleaning and preprocessing**:
  - The project includes scripts for data cleaning to ensure the dataset is free of errors and inconsistencies.
  - Preprocessing steps include handling missing values, outlier detection, and normalization of data, making it ready for analysis.

- **Future work**:
  - The next phase involves data mining on the cleaned dataset to identify correlations between gas concentrations and the ripening stages of fruits.
  - Advanced statistical analysis and machine learning techniques will be applied to discover patterns and insights.
  - Visualizations will be created to represent the relationship between gas levels and fruit ripening over time.

## Usage

1. **Assemble the hardware**: Connect the SGP30, HTU21, and SHT20 sensors to the ESP8266 NodeMCU.
2. **Upload the Arduino sketch**: Use the Arduino IDE to upload `main.ino` to the ESP8266.
3. **Start the Python server**: Run `server.py` to start the server.
4. **Begin data collection**: The sensors will start collecting data and sending it to the server, which will store it in the SQLite database.

## Report Images

- **Banana Ripening Images**:

  Day 1 (11 Nov)  
  ![Day 1](doc/readme/day1.jpg)  

  Day 2 (12 Nov)  
  ![Day 2](doc/readme/day2.jpg)  

  Day 3 (13 Nov)  
  ![Day 3](doc/readme/day3.jpg)  

  Day 4 (14 Nov)  
  ![Day 4](doc/readme/day4.jpg)  

  Day 5 (15 Nov)  
  ![Day 5](doc/readme/day5.jpg)  

  Day 6 (16 Nov)  
  ![Day 6](doc/readme/day6.jpg)  

- **Data Correlation Charts**:

  Gas correlation charts from 11 Nov to 16 Nov (the black line indicates when the banana was in perfect shape).

  VOC hourly chart  
  ![VOC](doc/readme/voc.png)  

  CO2 and VOC hourly chart  
  ![CO2](doc/readme/co2.png)  

  H2 and VOC hourly chart  
  ![H2](doc/readme/h2.png)  

  Ethanol and VOC hourly chart  
  ![Ethanol](doc/readme/ethanol.png)  

  Temperature and VOC hourly chart  
  ![Temperature](doc/readme/temperature.png)  

  Humidity and VOC hourly chart  
  ![Humidity](doc/readme/humidity.png)  

## Future Work

- **Data Mining**: Analyze the cleaned dataset to find correlations between VOC gases and fruit ripening.
- **Visualization**: Develop visualizations to better understand the relationship between gas levels and the ripening process.
- **Optimization**: Improve the accuracy and efficiency of data collection and analysis.

## Conclusion

This project provides a robust system for monitoring and analyzing fruit ripening using VOC gas sensors and temperature/humidity sensors. The collected data can be used for further analysis to uncover valuable insights into the ripening process.

