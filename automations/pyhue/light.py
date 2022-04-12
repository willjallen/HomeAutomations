import json
import automations.pyhue.patched_request as requests
import environment as env

class Light:
	def __init__(self, bridge, data):
		self.bridge = bridge
		self.data = data
		self.url = env.url + '/light/' + self.getID()
	
		self.duration_payload = {'dyanmics' : {'duration' : 0}}


	def turnOn(self):
		payload = {'on' : {'on' : True}}
		return self.sendData(payload)

	def turnOff(self):
		payload = {'on' : {'on' : False}}

	def getOnOffState(self):
		return self.data['on']['on']

	def setDimming(self, brightness):
		payload = {'dimming' : {'brightness' : brightness}}
		return self.sendData(payload)

	def getDimming():
		return self.data['dimming']['brightness']

	# id: (string – pattern: ^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$)
	# Unique identifier representing a specific resource instance
	def getID(self):
		return self.data['id']

	# [153, 500], 500 is more red, 153 more blue
	def setColorTemperature(self, temp):
		payload = {'color_temperature': {'mirek': temp}}
		return self.sendData(payload)

	def setColorXY(self, x, y):
		payload = {'color': {'xy' : {'x': x, 'y': y}}}
		return self.sendData(payload)

	def setColorGamut(self, r_x, r_y, g_x, g_y, b_x, b_y):
		payload = {'gamut' : 
			{	
				{'red' : {'x' : r_x, 'y': r_y}},
				{'green' : {'x': g_x, 'y': g_y}},
				{'blue' : {'x' : b_x, 'y' : b_y}}
			}
		}

	# Note: this state is appended to every request
	# maximum: 6000000ms
	def setDuration(self, duration):
		self.duration_payload = {'dynamics' : {'duration' : duration}}

	def getData(self):
		response = requests.get(url=env.url + '/light')
		self.data = response.json()

	def sendData(self, payload):
		payload.update(self.duration_payload)
		print(payload)
		response = requests.put(url=self.url, json=payload)
		self.getData()
		return response

		

