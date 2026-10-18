import requests

# URL = https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=tle

def get_satellites():
  try:
    # FIXME: Complete the get request
    response = requests.get(
      URL,

    )
  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except requests.exceptions.Timeout:
    print("The request timed out.")
  except requests.exceptions.RequestException as err:
    print(f"A system or network error occurred: {err}")