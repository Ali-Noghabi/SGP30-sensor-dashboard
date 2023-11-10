-- Create sensor_data_minutely_avg_of_avgs table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_avg_of_avgs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sensor TEXT,
       minute_start TEXT,
       avg_of_avg_tvoc REAL,
       avg_of_avg_eco2 REAL,
       avg_of_avg_rawh2 REAL,
       avg_of_avg_rawethanol REAL,
       avg_of_avg_temperature REAL,
       avg_of_avg_humidity REAL
);
-- Insert into sensor_data_minutely_avg_of_avgs table
INSERT INTO sensor_data_minutely_avg_of_avgs (
              sensor,
              minute_start,
              avg_of_avg_tvoc,
              avg_of_avg_eco2,
              avg_of_avg_rawh2,
              avg_of_avg_rawethanol,
              avg_of_avg_temperature,
              avg_of_avg_humidity
       )
SELECT sensor,
       strftime('%Y-%m-%d %H:%M:00', timestamp) AS minute_start,
       AVG(tvoc) AS avg_of_avg_tvoc,
       AVG(eco2) AS avg_of_avg_eco2,
       AVG(rawh2) AS avg_of_avg_rawh2,
       AVG(rawethanol) AS avg_of_avg_rawethanol,
       AVG(temperature) AS avg_of_avg_temperature,
       AVG(humidity) AS avg_of_avg_humidity
FROM sensor_data
GROUP BY sensor,
       strftime('%Y-%m-%d %H:%M:00', timestamp);
-- Create sensor_data_minutely_max_of_maxs table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_max_of_maxs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sensor TEXT,
       timestamp TEXT,
       tvoc REAL,
       eco2 REAL,
       rawh2 REAL,
       rawethanol REAL,
       temperature REAL,
       humidity REAL
);
-- Insert into sensor_data_minutely_max_of_maxs table
INSERT INTO sensor_data_minutely_max_of_maxs (
              sensor,
              timestamp,
              tvoc,
              eco2,
              rawh2,
              rawethanol,
              temperature,
              humidity
       )
SELECT sensor,
       strftime('%Y-%m-%d %H:%M:00', timestamp) AS timestamp,
       MAX(tvoc) AS tvoc,
       MAX(eco2) AS eco2,
       MAX(rawh2) AS rawh2,
       MAX(rawethanol) AS rawethanol,
       MAX(temperature) AS temperature,
       MAX(humidity) AS humidity
FROM sensor_data
GROUP BY sensor,
       strftime('%Y-%m-%d %H:%M:00', timestamp);
-- Create sensor_data_minutely_min_of_mins table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_min_of_mins (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sensor TEXT,
       timestamp TEXT,
       tvoc REAL,
       eco2 REAL,
       rawh2 REAL,
       rawethanol REAL,
       temperature REAL,
       humidity REAL
);
-- Insert into sensor_data_minutely_min_of_mins table
INSERT INTO sensor_data_minutely_min_of_mins (
              sensor,
              timestamp,
              tvoc,
              eco2,
              rawh2,
              rawethanol,
              temperature,
              humidity
       )
SELECT sensor,
       strftime('%Y-%m-%d %H:%M:00', timestamp) AS timestamp,
       MIN(tvoc) AS tvoc,
       MIN(eco2) AS eco2,
       MIN(rawh2) AS rawh2,
       MIN(rawethanol) AS rawethanol,
       MIN(temperature) AS temperature,
       MIN(humidity) AS humidity
FROM sensor_data
GROUP BY sensor,
       strftime('%Y-%m-%d %H:%M:00', timestamp);
-- Create sensor_data_hourly_avg_of_avgs table
CREATE TABLE IF NOT EXISTS sensor_data_hourly_avg_of_avgs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sensor TEXT,
       timestamp TEXT,
       tvoc REAL,
       eco2 REAL,
       rawh2 REAL,
       rawethanol REAL,
       temperature REAL,
       humidity REAL
);
-- Insert into sensor_data_hourly_avg_of_avgs table
INSERT INTO sensor_data_hourly_avg_of_avgs (
              sensor,
              timestamp,
              tvoc,
              eco2,
              rawh2,
              rawethanol,
              temperature,
              humidity
       )
SELECT sensor,
       strftime('%Y-%m-%d %H:00:00', timestamp) AS timestamp,
       AVG(tvoc) AS tvoc,
       AVG(eco2) AS eco2,
       AVG(rawh2) AS rawh2,
       AVG(rawethanol) AS rawethanol,
       AVG(temperature) AS temperature,
       AVG(humidity) AS humidity
FROM sensor_data
GROUP BY sensor,
       strftime('%Y-%m-%d %H:00:00', timestamp);
-- Create sensor_data_hourly_max_of_maxs table
CREATE TABLE IF NOT EXISTS sensor_data_hourly_max_of_maxs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sensor TEXT,
       timestamp TEXT,
       tvoc REAL,
       eco2 REAL,
       rawh2 REAL,
       rawethanol REAL,
       temperature REAL,
       humidity REAL
);
-- Insert into sensor_data_hourly_max_of_maxs table
INSERT INTO sensor_data_hourly_max_of_maxs (
              sensor,
              timestamp,
              tvoc,
              eco2,
              rawh2,
              rawethanol,
              temperature,
              humidity
       )
SELECT sensor,
       strftime('%Y-%m-%d %H:00:00', timestamp) AS timestamp,
       MAX(tvoc) AS tvoc,
       MAX(eco2) AS eco2,
       MAX(rawh2) AS rawh2,
       MAX(rawethanol) AS rawethanol,
       MAX(temperature) AS temperature,
       MAX(humidity) AS humidity
FROM sensor_data
GROUP BY sensor,
       strftime('%Y-%m-%d %H:00:00', timestamp);
-- Create sensor_data_hourly_min_of_mins table
CREATE TABLE IF NOT EXISTS sensor_data_hourly_min_of_mins (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       sensor TEXT,
       timestamp TEXT,
       tvoc REAL,
       eco2 REAL,
       rawh2 REAL,
       rawethanol REAL,
       temperature REAL,
       humidity REAL
);
-- Insert into sensor_data_hourly_min_of_mins table
INSERT INTO sensor_data_hourly_min_of_mins (
              sensor,
              timestamp,
              tvoc,
              eco2,
              rawh2,
              rawethanol,
              temperature,
              humidity
       )
SELECT sensor,
       strftime('%Y-%m-%d %H:00:00', timestamp) AS timestamp,
       MIN(tvoc) AS tvoc,
       MIN(eco2) AS eco2,
       MIN(rawh2) AS rawh2,
       MIN(rawethanol) AS rawethanol,
       MIN(temperature) AS temperature,
       MIN(humidity) AS humidity
FROM sensor_data
GROUP BY sensor,
       strftime('%Y-%m-%d %H:00:00', timestamp);