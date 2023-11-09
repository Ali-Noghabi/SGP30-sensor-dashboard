
import sqlite3
conn = sqlite3.connect('sensor_data.db') #linux
cursor = conn.cursor()
cursor.execute('''
-- Create sensor_data_minutely table
CREATE TABLE IF NOT EXISTS sensor_data_minutely AS
SELECT 
    NULL AS id, 
    sensor, 
    strftime('%Y-%m-%d %H:%M:00', timestamp) AS minute_start,
    AVG(tvoc) AS avg_tvoc,
    AVG(eco2) AS avg_eco2,
    AVG(rawh2) AS avg_rawh2,
    AVG(rawethanol) AS avg_rawethanol,
    AVG(temperature) AS avg_temperature,
    AVG(humidity) AS avg_humidity
FROM sensor_data
GROUP BY sensor, strftime('%Y-%m-%d %H:%M:00', timestamp);''')

cursor.execute('''
-- Create sensor_data_hourly table
CREATE TABLE IF NOT EXISTS sensor_data_hourly AS
SELECT 
    NULL AS id, 
    sensor, 
    strftime('%Y-%m-%d %H:00:00', timestamp) AS hour_start,
    AVG(tvoc) AS avg_tvoc,
    AVG(eco2) AS avg_eco2,
    AVG(rawh2) AS avg_rawh2,
    AVG(rawethanol) AS avg_rawethanol,
    AVG(temperature) AS avg_temperature,
    AVG(humidity) AS avg_humidity
FROM sensor_data
GROUP BY sensor, strftime('%Y-%m-%d %H:00:00', timestamp);''')



#remove outlier
# CREATE TEMPORARY TABLE temp_sensor_data AS
# SELECT 
#     sensor, 
#     timestamp,
#     tvoc,
#     eco2,
#     rawh2,
#     rawethanol,
#     temperature,
#     humidity
# FROM sensor_data
# WHERE 
#     timestamp NOT IN (
#         SELECT timestamp
#         FROM (
#             SELECT timestamp,
#                    ABS(tvoc - (SELECT AVG(tvoc) FROM sensor_data)) AS tvoc_diff,
#                    ABS(eco2 - (SELECT AVG(eco2) FROM sensor_data)) AS eco2_diff,
#                    ABS(rawh2 - (SELECT AVG(rawh2) FROM sensor_data)) AS rawh2_diff,
#                    ABS(rawethanol - (SELECT AVG(rawethanol) FROM sensor_data)) AS rawethanol_diff,
#                    ABS(temperature - (SELECT AVG(temperature) FROM sensor_data)) AS temperature_diff,
#                    ABS(humidity - (SELECT AVG(humidity) FROM sensor_data)) AS humidity_diff
#             FROM sensor_data
#         )
#         WHERE 
#             tvoc_diff > 1.5 * (SELECT MAX(tvoc_diff) FROM (SELECT ABS(tvoc - (SELECT AVG(tvoc) FROM sensor_data)) AS tvoc_diff FROM sensor_data)) OR
#             eco2_diff > 1.5 * (SELECT MAX(eco2_diff) FROM (SELECT ABS(eco2 - (SELECT AVG(eco2) FROM sensor_data)) AS eco2_diff FROM sensor_data)) OR
#             rawh2_diff > 1.5 * (SELECT MAX(rawh2_diff) FROM (SELECT ABS(rawh2 - (SELECT AVG(rawh2) FROM sensor_data)) AS rawh2_diff FROM sensor_data)) OR
#             rawethanol_diff > 1.5 * (SELECT MAX(rawethanol_diff) FROM (SELECT ABS(rawethanol - (SELECT AVG(rawethanol) FROM sensor_data)) AS rawethanol_diff FROM sensor_data)) OR
#             temperature_diff > 1.5 * (SELECT MAX(temperature_diff) FROM (SELECT ABS(temperature - (SELECT AVG(temperature) FROM sensor_data)) AS temperature_diff FROM sensor_data)) OR
#             humidity_diff > 1.5 * (SELECT MAX(humidity_diff) FROM (SELECT ABS(humidity - (SELECT AVG(humidity) FROM sensor_data)) AS humidity_diff FROM sensor_data))
#     );

# -- Replace the sensor_data table with the filtered data
# DELETE FROM sensor_data;

# INSERT INTO sensor_data (sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity)
# SELECT sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity
# FROM temp_sensor_data;

# -- Drop the temporary table
# DROP TABLE temp_sensor_data;


