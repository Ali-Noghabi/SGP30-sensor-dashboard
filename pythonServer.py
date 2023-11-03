import asyncio
import websockets
import json
import sqlite3
from datetime import datetime

# Create or connect to the SQLite database
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()
hostname = "localhost"
port = 5000

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor TEXT,
        timestamp TEXT,
        tvoc REAL,
        eco2 REAL,
        rawh2 REAL,
        rawethanol REAL,
        temperature REAL,
        humidity REAL
    )
''')

async def handle_websocket(websocket):
    async for message in websocket:
        print(f"Received message: {message}")
        if str(message).startswith("getOnlineData"):
            data = fetch_last_data_from_database()
            json_data = json.dumps(data)
            await websocket.send(json_data)
        elif str(message).startswith("getHistorianData"):
            mesList = str(message).split("|" , 3)
            data = fetch_data_between_timestamps(mesList[1] , mesList[2])
            json_data = json.dumps(data)
            print(json_data)
            await websocket.send(json_data)
        else:
            try:
                data = json.loads(message)
                name = data["name"]
                tvoc = data["TVOC"]
                eco2 = data["eCO2"]
                rawh2 = data["rawH2"]
                rawethanol = data["rawEthanol"]
                temperature = data["Temperature"]
                humidity = data["Humidity"]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f"Name: {name},TVOC: {tvoc}, eCO2: {eco2}, rawH2: {rawh2}, rawEthanol: {rawethanol},Temperature: {temperature},Humidity: {humidity}, Timestamp: {timestamp}")
                insert_data_into_database(name ,timestamp, tvoc, eco2, rawh2, rawethanol , temperature ,humidity )
            except Exception as e:
                print(f"Error parsing message: {e}")
            await websocket.send("Message received")

def fetch_last_data_from_database():
    cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        data = {
            "Sensor":row[1],
            "TVOC": row[3],
            "eCO2": row[4],
            "rawH2": row[5],
            "rawEthanol": row[6],
            "Timestamp": row[2]
        }
    else:
        data = {}
    return data

def fetch_data_between_timestamps(start_timestamp, end_timestamp):
    query = 'SELECT * FROM sensor_data WHERE timestamp >= ? AND timestamp <= ?'
    cursor.execute(query, (start_timestamp, end_timestamp))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        data = {
            "Sensor":row[1],
            "TVOC": row[3],
            "eCO2": row[4],
            "rawH2": row[5],
            "rawEthanol": row[6],
            "Temperature": row[7],
            "Humidity": row[8],
            "Timestamp": row[2]
        }
        result.append(data)
    return result

def insert_data_into_database(sensor ,timestamp, tvoc, eco2, rawh2, rawethanol ,temperature , humidity):
    cursor.execute('''
        INSERT INTO sensor_data (sensor ,timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity)
        VALUES (? ,?, ?, ?, ?, ? , ? , ?)
    ''', (sensor , timestamp, tvoc, eco2, rawh2, rawethanol , temperature , humidity))
    conn.commit()

async def main():
    async with websockets.serve(handle_websocket, hostname, port):
        print("Server started")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
