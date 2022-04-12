import requests
import environment as env
import json

# https://www.weatherapi.com/docs/

url = 'https://api.weatherapi.com/v1'

current_weather_url = '/current.json'
forecast_url = '/forecast.json'
astronomy_url = '/astronomy.json'

payload = {'key': str(env.weather_api_key), 'q': str(env.weather_api_location)}

class WeatherController():
	def __init__(self, master_controller):
		self.master_controller = master_controller
		self.weather_json = None
		self.forcecast_json = None
		self.astronomy_json = {'sunrise': '06:45 AM', 'sunset': '05:30 PM', 'moonrise': '03:55 PM', 'moonset': '04:51 AM', 'moon_phase': 'First Quarter', 'moon_illumination': '73'}


	def retrieve_current_weather(self):
		response = requests.get(url+current_weather_url, params=payload)
		self.weather_json = json.loads(response.text)

	def retrieve_forecast(self):
		response = requests.get(url+forecast_url, params=payload)
		self.forecast_json = json.loads(response.text)

	def retrieve_astronomy(self):
		response = requests.get(url+astronomy_url, params=payload)
		self.astronomy_json = (json.loads(response.text))['astronomy']['astro']
		print(self.astronomy_json)

	def retrieve_all(self):
		self.retrieve_current_weather()
		self.retrieve_forecast()
		self.retrieve_astronomy()



# weather_controller.retrieve_all()

# print()
# print(json.dumps(weather_controller.weather_json, indent=4))
# print()
# print(json.dumps(weather_controller.forecast_json, indent=4))