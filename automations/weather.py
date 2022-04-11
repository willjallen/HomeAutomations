import requests
import environment
# https://www.weatherapi.com/docs/

url = 'https://api.weatherapi.com/v1'

current_weather_url = '/current.json'
forecast_url = '/forecast.json'
astronomy_url = 'astronomy.josn'

payload = ('key': str(environment.weather_api_key), 'q': str(environment.weather_api_location))

class WeatherController():
	def __init__(self):
		self.weather_json = None
		self.forcecast_json = None
		self.astronomy_json = None



	def retrieve_all(self)
		retrieve_current_weather()
		retrieve_forecast()
		retrieve_astronomy()

	def retrieve_current_weather(self):
		response = requests.get(url+current_weather_url, params=payload)
		self.weather_json = response.json()

	def retrieve_forecast(self):
		response = requests.get(url+forecast_url, params=payload)
		self.forecast_json = response.json()

	def retrieve_astronomy(self):
		response = requests.get(url+astronomy_url, params=payload)
		self.astronomy_json = response.json()
