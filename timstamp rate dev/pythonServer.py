import asyncio
import websockets
import json
import sqlite3
from datetime import datetime

# Create or connect to the SQLite database
# test
# conn = sqlite3.connect('databases\main.db')  # windows
conn = sqlite3.connect('databases/main.db') #linux
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
        try:
            received_data = json.loads(message)
            if received_data["request-type"] == "getHistorianData":
                timestamp_rate = received_data["timestamp-rate"]
                data_types = received_data["data-types"]
                sensors = received_data["sensors"]
                start_time = received_data["start-time"]
                end_time = received_data["end-time"]
                data = fetch_data_between_timestamps(
                    start_time, end_time, timestamp_rate, data_types, sensors)
                json_data = json.dumps(data)
                print(json_data)
                await websocket.send(json_data)
        except Exception as e:
            print(f"Error parsing message: {e}")
        print(f"Received message: {message}")
        # if str(message).startswith("getOnlineData"):
        #     data = fetch_last_data_from_database()
        #     json_data = json.dumps(data)
        #     await websocket.send(json_data)
        # if received_data["request-type"] == "getHistorianData":
        #     timestamp_rate = received_data["timestamp-rate"]
        #     data_types = received_data["data-types"]
        #     sensors = received_data["sensors"]
        #     start_time = received_data["start-time"]
        #     end_time = received_data["end-time"]
        #     data = fetch_data_between_timestamps(start_time, end_time, timestamp_rate, data_types, sensors)
        #     json_data = json.dumps(data)
        #     print(json_data)
        #     await websocket.send(json_data)
        # else:
        #     try:
        #         data = json.loads(message)
        #         name = data["name"]
        #         tvoc = data["TVOC"]
        #         eco2 = data["eCO2"]
        #         rawh2 = data["rawH2"]
        #         rawethanol = data["rawEthanol"]
        #         temperature = data["Temperature"]
        #         humidity = data["Humidity"]
        #         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #         print(
        #             f"Name: {name},TVOC: {tvoc}, eCO2: {eco2}, rawH2: {rawh2}, rawEthanol: {rawethanol},Temperature: {temperature},Humidity: {humidity}, Timestamp: {timestamp}")
        #         insert_data_into_database(name ,timestamp, tvoc, eco2, rawh2, rawethanol , temperature ,humidity )
        #     except Exception as e:
        #         print(f"Error parsing message: {e}")
        #     await websocket.send("Message received")


def fetch_last_data_from_database():
    cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        data = {
            "Sensor": row[1],
            "TVOC": row[3],
            "eCO2": row[4],
            "rawH2": row[5],
            "rawEthanol": row[6],
            "Timestamp": row[2]
        }
    else:
        data = {}
    return data


def fetch_data_between_timestamps(start_time, end_time, timestamp_rate, data_types, sensors):
    print("to fetch" , start_time, end_time, timestamp_rate, data_types, sensors)
    result = {}

    for data_type in data_types:
        query = 'SELECT * FROM sensor_data_{}_{} WHERE timestamp >= ? AND timestamp <= ?'.format(
            timestamp_rate, data_type)

        print("query: ", query)
        cursor.execute(query, (start_time, end_time))  # Use parameterized query to avoid SQL injection
        rows = cursor.fetchall()

        result[data_type] = []
        for row in rows:
            data = {
                "Sensor": row[1],
                "Timestamp": row[2]
            }
            # Add columns to data only if the corresponding value is not None
            if "tvoc" in sensors and row[3] is not None:
                data["TVOC"] = row[3]
            if "eco2" in sensors and row[4] is not None:
                data["eCO2"] = row[4]
            if "rawh2" in sensors and row[5] is not None:
                data["rawH2"] = row[5]
            if "rawethanol" in sensors and row[6] is not None:
                data["rawEthanol"] = row[6]
            if "temperature" in sensors and row[7] is not None:
                data["Temperature"] = row[7]
            if "humidity" in sensors and row[8] is not None:
                data["Humidity"] = row[8]
            result[data_type].append(data)

    return result



def insert_data_into_database(sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity):
    cursor.execute('''
        INSERT INTO sensor_data (sensor ,timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity)
        VALUES (? ,?, ?, ?, ?, ? , ? , ?)
    ''', (sensor, timestamp, tvoc, eco2, rawh2, rawethanol, temperature, humidity))
    conn.commit()


async def main():
    async with websockets.serve(handle_websocket, hostname, port):
        print("Server started")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
