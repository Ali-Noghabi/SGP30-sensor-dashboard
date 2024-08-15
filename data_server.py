import asyncio
import websockets
import json
import sqlite3
from datetime import datetime, timezone

# Create or connect to the SQLite database
conn = sqlite3.connect('databases/sensors_database.db')  # Adjust path as needed
cursor = conn.cursor()
hostname = "192.168.2.153"
port = 5000

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor TEXT,
        timestamp TEXT,
        tvoc REAL,
        eco2 REAL,
        rawh2 REAL,
        rawethanol REAL,
        temperature REAL,
        humidity REAL,
        moisture REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS minutely_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor TEXT,
        timestamp TEXT,
        avg_tvoc REAL,
        avg_eco2 REAL,
        avg_rawh2 REAL,
        avg_rawethanol REAL,
        avg_temperature REAL,
        avg_humidity REAL,
        avg_moisture REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS hourly_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor TEXT,
        timestamp TEXT,
        avg_tvoc REAL,
        avg_eco2 REAL,
        avg_rawh2 REAL,
        avg_rawethanol REAL,
        avg_temperature REAL,
        avg_humidity REAL,
        avg_moisture REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor TEXT,
        timestamp TEXT,
        avg_tvoc REAL,
        avg_eco2 REAL,
        avg_rawh2 REAL,
        avg_rawethanol REAL,
        avg_temperature REAL,
        avg_humidity REAL,
        avg_moisture REAL
    )
''')

# Function to insert sensor data into the database
def insert_data_into_database(sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity, moisture):
    cursor.execute('''
        INSERT INTO raw_data (sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity, moisture)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity, moisture))
    conn.commit()

# Functions to calculate summaries
def calculate_minutely_summary():
    cursor.execute('''
        SELECT sensor,
               strftime('%Y-%m-%d %H:%M:00', timestamp) as minute,
               AVG(tvoc), AVG(eco2), AVG(rawh2), AVG(rawethanol), AVG(temperature), AVG(humidity), AVG(moisture)
        FROM raw_data
        WHERE timestamp >= datetime('now', '-1 minute')
        AND timestamp < datetime('now')
        AND minute NOT IN (SELECT timestamp FROM minutely_summary)
        GROUP BY sensor, minute
    ''')

    results = cursor.fetchall()

    if results:
        cursor.executemany('''
            INSERT INTO minutely_summary (sensor, timestamp, avg_tvoc, avg_eco2, avg_rawh2, avg_rawethanol, avg_temperature, avg_humidity, avg_moisture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', results)
        conn.commit()

def calculate_hourly_summary():
    cursor.execute('''
        SELECT sensor,
               strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
               AVG(tvoc), AVG(eco2), AVG(rawh2), AVG(rawethanol), AVG(temperature), AVG(humidity), AVG(moisture)
        FROM raw_data
        WHERE timestamp >= datetime('now', '-1 hour')
        AND timestamp < datetime('now')
        AND hour NOT IN (SELECT timestamp FROM hourly_summary)
        GROUP BY sensor, hour
    ''')

    results = cursor.fetchall()

    if results:
        cursor.executemany('''
            INSERT INTO hourly_summary (sensor, timestamp, avg_tvoc, avg_eco2, avg_rawh2, avg_rawethanol, avg_temperature, avg_humidity, avg_moisture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', results)
        conn.commit()

def calculate_daily_summary():
    cursor.execute('''
        SELECT sensor,
               strftime('%Y-%m-%d 00:00:00', timestamp) as day,
               AVG(tvoc), AVG(eco2), AVG(rawh2), AVG(rawethanol), AVG(temperature), AVG(humidity), AVG(moisture)
        FROM raw_data
        WHERE timestamp >= datetime('now', '-1 day')
        AND timestamp < datetime('now')
        AND day NOT IN (SELECT timestamp FROM daily_summary)
        GROUP BY sensor, day
    ''')

    results = cursor.fetchall()

    if results:
        cursor.executemany('''
            INSERT INTO daily_summary (sensor, timestamp, avg_tvoc, avg_eco2, avg_rawh2, avg_rawethanol, avg_temperature, avg_humidity, avg_moisture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', results)
        conn.commit()

# WebSocket handler
async def handle_websocket(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            try:
                data = json.loads(message)
                name = data["name"]
                tvoc = data["TVOC"]
                eco2 = data["eCO2"]
                rawh2 = data["rawH2"]
                rawethanol = data["rawEthanol"]
                temperature = data["Temperature"]
                humidity = data["Humidity"]
                moisture = data["moisture"]  # New data field for moisture

                timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                print(f"Name: {name}, TVOC: {tvoc}, eCO2: {eco2}, rawH2: {rawh2}, rawEthanol: {rawethanol}, Temperature: {temperature}, Humidity: {humidity}, Moisture: {moisture}, Timestamp: {timestamp}")
                insert_data_into_database(name, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity, moisture)
            except Exception as e:
                print(f"Error parsing message: {e}")
            await websocket.send("Message received")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

# Timer functions
async def minutely_summary_timer():
    while True:
        calculate_minutely_summary()
        await asyncio.sleep(60)  # Trigger every minute

async def hourly_summary_timer():
    while True:
        calculate_hourly_summary()
        await asyncio.sleep(3600)  # Trigger every hour

async def daily_summary_timer():
    while True:
        calculate_daily_summary()
        await asyncio.sleep(86400)  # Trigger every day

async def main():
    minutely_task = asyncio.create_task(minutely_summary_timer())
    hourly_task = asyncio.create_task(hourly_summary_timer())
    daily_task = asyncio.create_task(daily_summary_timer())

    async with websockets.serve(handle_websocket, hostname, port, ping_timeout=20, ping_interval=20):
        print("Server started")
        await asyncio.gather(minutely_task, hourly_task, daily_task)

if __name__ == "__main__":
    asyncio.run(main())