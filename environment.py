import os
from dotenv import load_dotenv




load_dotenv()
weather_api_key = os.getenv("WEATHER-API-KEY")
weather_api_location = os.getenv("WEATHER-API-LOC")

time_zone = os.getenv("TIME-ZONE")


hue_application_key = os.getenv("HUE-APPLICATION-KEY")
hue_bridge_id = os.getenv("HUE-BRIDGE-ID")

url = os.getenv("URL")
cert = os.getenv("CERT")

