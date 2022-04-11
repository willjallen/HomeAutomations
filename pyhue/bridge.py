import environment as env
import json
import patched_request as requests

from light import Light

class Bridge():
	def __init__(self):
		self.lights = []
		self.getLightData()
		

	def getLights(self):
		return self.lights


	def getLightData(self):

		response = requests.get(url=env.url + '/light')
		
		lightsData = response.json()['data']

		self.numLights = len(lightsData)
		print(json.dumps(lightsData, indent=4))
		for i in range(0, len(lightsData)):
			light = Light(bridge=self, data=lightsData[i])
			if(i >= len(self.lights)):
				self.lights.append(light)	
			else:
				self.lights[i] = light  

		# for light in self.lights:
		# 	light.setDuration(10000)
		# 	response = light.setDimming(20)
		# 	print(response)

# bridge = Bridge()
# bridge.getLightData()