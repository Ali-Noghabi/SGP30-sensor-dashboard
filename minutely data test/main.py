import sqlite3
conn = sqlite3.connect('sensor_data.db') #linux
cursor = conn.cursor()

cursor.execute('''
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
GROUP BY sensor, strftime('%Y-%m-%d %H:%M:00', timestamp);
''')
