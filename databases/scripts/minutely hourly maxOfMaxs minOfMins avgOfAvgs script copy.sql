-- Create sensor_data_minutely_avg_of_avgs table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_avg_of_avgs (
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

-- Insert into sensor_data_minutely_avg_of_avgs table
INSERT INTO sensor_data_minutely_avg_of_avgs (sensor, minute_start, avg_of_avg_tvoc, avg_of_avg_eco2, avg_of_avg_rawh2, avg_of_avg_rawethanol, avg_of_avg_temperature, avg_of_avg_humidity)
SELECT sensor, strftime('%Y-%m-%d %H:%M:00', timestamp) AS minute_start,
       AVG(tvoc) AS avg_of_avg_tvoc,
       AVG(eco2) AS avg_of_avg_eco2,
       AVG(rawh2) AS avg_of_avg_rawh2,
       AVG(rawethanol) AS avg_of_avg_rawethanol,
       AVG(temperature) AS avg_of_avg_temperature,
       AVG(humidity) AS avg_of_avg_humidity
FROM sensor_data
GROUP BY sensor, strftime('%Y-%m-%d %H:%M:00', timestamp);


-- Create sensor_data_minutely_avg_of_avgs table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_avg_of_avgs AS
  SELECT NULL                                     AS id,
         sensor,
         Strftime('%Y-%m-%d %H:%M:00', timestamp) AS timestamp,
         Avg(tvoc)                            AS tvoc,
         Avg(eco2)                            AS eco2,
         Avg(rawh2)                           AS rawh2,
         Avg(rawethanol)                      AS rawethanol,
         Avg(temperature)                     AS temperature,
         Avg(humidity)                        AS humidity
  FROM   sensor_data
  GROUP  BY sensor,
            Strftime('%Y-%m-%d %H:%M:00', timestamp);

-- Create sensor_data_minutely_max_of_maxs table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_max_of_maxs AS
  SELECT NULL                                     AS id,
         sensor,
         Strftime('%Y-%m-%d %H:%M:00', timestamp) AS timestamp,
         Max(tvoc)                            AS tvoc,
         Max(eco2)                            AS eco2,
         Max(rawh2)                           AS rawh2,
         Max(rawethanol)                      AS rawethanol,
         Max(temperature)                     AS temperature,
         Max(humidity)                        AS humidity
  FROM   sensor_data
  GROUP  BY sensor,
            Strftime('%Y-%m-%d %H:%M:00', timestamp);

-- Create sensor_data_minutely_min_of_mins table
CREATE TABLE IF NOT EXISTS sensor_data_minutely_min_of_mins AS
  SELECT NULL                                     AS id,
         sensor,
         Strftime('%Y-%m-%d %H:%M:00', timestamp) AS timestamp,
         Min(tvoc)                            AS tvoc,
         Min(eco2)                            AS eco2,
         Min(rawh2)                           AS rawh2,
         Min(rawethanol)                      AS rawethanol,
         Min(temperature)                     AS temperature,
         Min(humidity)                        AS humidity
  FROM   sensor_data
  GROUP  BY sensor,
            Strftime('%Y-%m-%d %H:%M:00', timestamp);

-- Create sensor_data_hourly_avg_of_avgs table
CREATE TABLE IF NOT EXISTS sensor_data_hourly_avg_of_avgs AS
  SELECT NULL                                     AS id,
         sensor,
         Strftime('%Y-%m-%d %H:00:00', timestamp) AS timestamp,
         Avg(tvoc)                            AS tvoc,
         Avg(eco2)                            AS eco2,
         Avg(rawh2)                           AS rawh2,
         Avg(rawethanol)                      AS rawethanol,
         Avg(temperature)                     AS temperature,
         Avg(humidity)                        AS humidity
  FROM   sensor_data
  GROUP  BY sensor,
            Strftime('%Y-%m-%d %H:00:00', timestamp);

-- Create sensor_data_hourly_max_of_maxs table
CREATE TABLE IF NOT EXISTS sensor_data_hourly_max_of_maxs AS
  SELECT NULL                                     AS id,
         sensor,
         Strftime('%Y-%m-%d %H:00:00', timestamp) AS timestamp,
         Max(tvoc)                            AS tvoc,
         Max(eco2)                            AS eco2,
         Max(rawh2)                           AS rawh2,
         Max(rawethanol)                      AS rawethanol,
         Max(temperature)                     AS temperature,
         Max(humidity)                        AS humidity
  FROM   sensor_data
  GROUP  BY sensor,
            Strftime('%Y-%m-%d %H:00:00', timestamp);

-- Create sensor_data_hourly_min_of_mins table
CREATE TABLE IF NOT EXISTS sensor_data_hourly_min_of_mins AS
  SELECT NULL                                     AS id,
         sensor,
         Strftime('%Y-%m-%d %H:00:00', timestamp) AS timestamp,
         Min(tvoc)                            AS tvoc,
         Min(eco2)                            AS eco2,
         Min(rawh2)                           AS rawh2,
         Min(rawethanol)                      AS rawethanol,
         Min(temperature)                     AS temperature,
         Min(humidity)                        AS humidity
  FROM   sensor_data
  GROUP  BY sensor,
            Strftime('%Y-%m-%d %H:00:00', timestamp); 