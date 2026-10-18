import requests
import os
from datetime import datetime, timedelta

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle" # all records

file_path = "./utils/satellite_data/active.csv"

def update_satellite_records():
  """This fetches data from Celestrak.org and saves the .csv locally to use 
  the satellite records for this project. The site limits fetches to once 
  every two hours. When two hours have passed since the last update of the
  file_path, a new fetch will be executed.
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

    else:
      print(f"\nData current. Next update can occur after {update_time.strftime("%H:%M:%S")}.\n")

  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except requests.exceptions.Timeout:
    print("The request timed out.")
  except requests.exceptions.RequestException as err:
    print(f"A system or network error occurred: {err}")

update_satellite_records()