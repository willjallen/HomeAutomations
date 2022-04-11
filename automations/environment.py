import os
from dotenv import load_dotenv

load_dotenv()
weather_api_key = os.getenv("WEATHER-API-KEY")
weather_api_location = os.getenv("WEATHER-API-LOC")

time_zone = os.getenv("TIME-ZONE")
