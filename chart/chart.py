import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

summary_frequency = "hourly"
data_base_path = "double_cleaned_sensors_database"

output_folder = f"{data_base_path}/{summary_frequency}_charts"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

conn = sqlite3.connect(f"{data_base_path}.db")

query = f"""
SELECT *
FROM {summary_frequency}_summary
"""

df = pd.read_sql_query(query, conn)

conn.close()

sensor1_data = df[df["sensor"] == "sensor1"].copy()
sensor2_data = df[df["sensor"] == "sensor2"].copy()

# Convert timestamp column to datetime format for better plotting
sensor1_data["timestamp"] = pd.to_datetime(sensor1_data["timestamp"])
sensor2_data["timestamp"] = pd.to_datetime(sensor2_data["timestamp"])

# List of parameters to plot
parameters = [
    "avg_tvoc",
    "avg_eco2",
    "avg_rawh2",
    "avg_rawethanol",
    "avg_temperature",
    "avg_humidity",
    "avg_moisture",
]

for param in parameters:
    plt.figure(figsize=(14, 8))

    plt.plot(
        sensor1_data["timestamp"],
        sensor1_data[param],
        label=f"sensor1 - {param}",
        marker="o",
    )

    plt.plot(
        sensor2_data["timestamp"],
        sensor2_data[param],
        label=f"sensor2 - {param}",
        marker="x",
    )

    plt.title(f"{param.capitalize()} Over Time for Sensor1 and Sensor2 in {summary_frequency} frequency")
    plt.xlabel("Timestamp")
    plt.ylabel(f"{param.capitalize()}")
    plt.legend(loc="upper left")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/{param}_over_time.png")
    plt.clf()

print(f"Charts saved successfully in the folder '{output_folder}'.")
