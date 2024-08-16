import sqlite3
import pandas as pd
from datetime import datetime
import numpy as np
from scipy import stats

# Original database path
original_db_path = 'cleaned_sensors_database.db'

# Cleaned database path
cleaned_db_path = 'duble_cleaned_sensors_database.db'

# Connect to the original database to read the data
conn_original = sqlite3.connect(original_db_path)
cursor_original = conn_original.cursor()

# Read raw data from the original database
raw_data_df = pd.read_sql_query("SELECT * FROM raw_data", conn_original)

# Data cleaning process
def clean_data(df):
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Handle missing values (if any)
    df = df.dropna()  # Option to fill with mean/median instead of dropping
    
    # Remove outliers using Z-score or IQR method (example with Z-score)
    df = df[(np.abs(stats.zscore(df.select_dtypes(include=[float, int]))) < 3).all(axis=1)]
    
    return df

# Clean the raw data
cleaned_raw_data_df = clean_data(raw_data_df)

# Close the connection to the original database
conn_original.close()

# Create a new cleaned database
conn_cleaned = sqlite3.connect(cleaned_db_path)
cursor_cleaned = conn_cleaned.cursor()

# Create the raw_data table in the new database and insert cleaned data
cursor_cleaned.execute('''
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
cleaned_raw_data_df.to_sql('raw_data', conn_cleaned, if_exists='replace', index=False)

# Function to create frequency-based summary tables
def create_summary_table(df, freq, table_name):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    
    # Group by the desired frequency and sensor, then calculate the mean
    summary_df = df.groupby([pd.Grouper(freq=freq), 'sensor']).mean().reset_index()

    # Rename columns to include 'avg_' prefix
    summary_df.columns = ['timestamp', 'sensor'] + [f'avg_{col}' for col in summary_df.columns if col not in ['timestamp', 'sensor']]
    
    # Create the summary table with cleaned summary data
    cursor_cleaned.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
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
    summary_df.to_sql(table_name, conn_cleaned, if_exists='replace', index=False)

# Create the summary tables in the new database
create_summary_table(cleaned_raw_data_df, 'T', 'minutely_summary')  # Minutely summary
create_summary_table(cleaned_raw_data_df, 'H', 'hourly_summary')   # Hourly summary
create_summary_table(cleaned_raw_data_df, 'D', 'daily_summary')    # Daily summary

# Commit changes and close the connection to the cleaned database
conn_cleaned.commit()
conn_cleaned.close()



