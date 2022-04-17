import json
import automations.pyhue.patched_request as requests
import environment as env

class Light:
	def __init__(self, bridge, data):
		self.bridge = bridge
		self.data = data
		self.url = env.url + '/light/' + self.get_ID()
	
		self.duration_payload = {'dyanmics' : {'duration' : 0}}


	def turn_on(self):
		payload = {'on' : {'on' : True}}
		return self.send_data(payload)

	def turn_off(self):
		payload = {'on' : {'on' : False}}

	def get_on_off_state(self):
		return self.data['on']['on']

	def set_brightness(self, brightness):
		payload = {'dimming' : {'brightness' : brightness}}
		return self.send_data(payload)

	def get_brightness():
		return self.data['dimming']['brightness']


	# id: (string – pattern: ^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$)
	# Unique identifier representing a specific resource instance
	def get_ID(self):
		return self.data['id']

	# [153, 500], 500 is more red, 153 more blue
	def set_color_temperature(self, temp):
		payload = {'color_temperature': {'mirek': temp}}
		return self.send_data(payload)

	def set_color_xy(self, x, y):
		payload = {'color': {'xy' : {'x': x, 'y': y}}}
		return self.send_data(payload)

	def set_color_gamut(self, r_x, r_y, g_x, g_y, b_x, b_y):
		payload = {'gamut' : 
			{	
				{'red' : {'x' : r_x, 'y': r_y}},
				{'green' : {'x': g_x, 'y': g_y}},
				{'blue' : {'x' : b_x, 'y' : b_y}}
			}
		}

	# Note: this state is appended to every request
	# maximum: 6000000ms
	def set_duration(self, duration):
		self.duration_payload = {'dynamics' : {'duration' : duration}}

	def flash_color(self, flash_durection, color):
		pass


	def get_data(self):
		response = requests.get(url=env.url + '/light')
		self.data = response.json()

	def send_data(self, payload):
		payload.update(self.duration_payload)
		print(payload)
		response = requests.put(url=self.url, json=payload)
		# self.retrieve_lights_data()
		return response

		

