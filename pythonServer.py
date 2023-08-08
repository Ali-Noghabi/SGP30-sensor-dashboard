import asyncio
import websockets
import json
import sqlite3
from datetime import datetime

# Create or connect to the SQLite database
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        tvoc REAL,
        eco2 REAL,
        rawh2 REAL,
        rawethanol REAL
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
                tvoc = data["TVOC"]
                eco2 = data["eCO2"]
                rawh2 = data["rawH2"]
                rawethanol = data["rawEthanol"]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f"TVOC: {tvoc}, eCO2: {eco2}, rawH2: {rawh2}, rawEthanol: {rawethanol}, Timestamp: {timestamp}")
                insert_data_into_database(timestamp, tvoc, eco2, rawh2, rawethanol)
            except Exception as e:
                print(f"Error parsing message: {e}")
            await websocket.send("Message received")

def fetch_last_data_from_database():
    cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        data = {
            "TVOC": row[2],
            "eCO2": row[3],
            "rawH2": row[4],
            "rawEthanol": row[5],
            "Timestamp": row[1]
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
            "TVOC": row[2],
            "eCO2": row[3],
            "rawH2": row[4],
            "rawEthanol": row[5],
            "Timestamp": row[1]
        }
        result.append(data)
    return result

def insert_data_into_database(timestamp, tvoc, eco2, rawh2, rawethanol):
    cursor.execute('''
        INSERT INTO sensor_data (timestamp, tvoc, eco2, rawh2, rawethanol)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, tvoc, eco2, rawh2, rawethanol))
    conn.commit()

async def main():
    async with websockets.serve(handle_websocket, "192.168.1.160", 5000):
        print("Server started")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
