import asyncpg
import asyncio
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

satellite_data_types = {
  'object_name': str, # "KUIPER-00008"
  'object_id': str, # "2025-088A",
  'epoch': str, # ? "2026-07-01T01:13:34.200192",
  'mean_motion': float, # 14.79922108,
  'eccentricity': float, # 7.625e-5,
  'inclination': float, # 51.9018,
  'raan': float, # 306.7242,
  'arg_of_pericenter': float, # 105.1798,
  'mean_anomaly': float, # 254.9249,
  'ephemeris_type': int, # 0,
  'classification_type': str, # "U",
  'norad_cat_id': int, # 63724,
  'element_set_no': int, # 999,
  'rev_at_epoch': int, # 6483,
  'bstar': float, # -0.00011397759,
  'mean_motion_dot': float, # -1.09e-5,
  'mean_motion_ddot': float # 0.0
}

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle" # all records

file_path = "./utils/satellite_data/active.csv"

async def load_csv_data(filename):
  df = pd.read_csv(filename, dtype=satellite_data_types)

  # Connect to target database
  conn = await asyncpg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("TARGET_DB")
  )

  await conn.execute('''
    DROP TABLE IF EXISTS satellites;

    CREATE TABLE satellites (
      object_id TEXT PRIMARY KEY,    
      object_name TEXT NOT NULL,
      epoch TEXT NOT NULL,
      mean_motion DOUBLE PRECISION NOT NULL,
      eccentricity REAL NOT NULL,
      inclination REAL NOT NULL,
      raan REAL NOT NULL,
      arg_of_pericenter REAL NOT NULL,
      mean_anomaly REAL NOT NULL,
      ephemeris_type SMALLINT NOT NULL,
      classification_type TEXT NOT NULL,
      norad_cat_id INTEGER NOT NULL,
      element_set_no SMALLINT NOT NULL,
      rev_at_epoch INTEGER NOT NULL,
      bstar DOUBLE PRECISION NOT NULL,
      mean_motion_dot DOUBLE PRECISION NOT NULL,
      mean_motion_ddot REAL NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  ''')

  table_name = "satellites"
  columns = [
    'object_name', 
    'object_id', 
    'epoch', 
    'mean_motion', 
    'eccentricity', 
    'inclination', 
    'raan', 
    'arg_of_pericenter', 
    'mean_anomaly', 
    'ephemeris_type', 
    'classification_type', 
    'norad_cat_id', 
    'element_set_no', 
    'rev_at_epoch', 
    'bstar', 
    'mean_motion_dot', 
    'mean_motion_ddot'
  ]
  satellite_records = [tuple(x) for x in df.to_numpy()]
  
  print(f"\nLoading {len(df)} satellite records...")

  await conn.copy_records_to_table(
    table_name,
    records=satellite_records,
    columns=columns
  )

  print(f"Loading of satellite.csv successful!\n")

  await conn.close()

async def update_satellite_records():
  """This fetches data from Celestrak.org and saves the .csv locally to use 
  the satellite records for this project. The site limits fetches to once 
  every two hours. When two hours have passed since the last update of the
  file_path, a new fetch will be executed and the database will be updated.
  """
  try:
    # Get time of last active.csv update)
    timestamp = os.path.getmtime(file_path)
    last_update = datetime.fromtimestamp(timestamp)

    # Next update can occur after two hours
    update_time = last_update + timedelta(hours=2)

    if datetime.now() > update_time:
      response = requests.get(
        URL,
        timeout=5
      )

      if response.status_code == 200:
        with open(file_path, "w", encoding="utf=8") as file:
          file.write(response.text)
        print("File updated successfully!")

        await load_csv_data(file_path)

    else:
      print(f"\nData current. Next update can occur after {update_time.strftime("%H:%M:%S")}.\n")

  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except requests.exceptions.Timeout:
    print("The request timed out.")
  except requests.exceptions.RequestException as err:
    print(f"A system or network error occurred: {err}")

async def main():
  await update_satellite_records()

if __name__ == "__main__":
  asyncio.run(main())