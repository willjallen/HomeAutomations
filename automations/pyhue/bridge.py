# import automations.pyhue.environment as env
import json
import automations.pyhue.patched_request as requests
import environment as env
from automations.pyhue.light import Light
from automations import constants

class BridgeController():
	def __init__(self, master_controller):
		self.master_controller = master_controller
		self.lights = []
		self.retrieve_lights_data()
		

	def get_lights(self):
		return self.lights


	def retrieve_lights_data(self):

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


	def update_light(self, **kwargs):
		pass


	def update_lights(self, **kwargs):
		
		action_type = kwargs['action_type']
		params = kwargs['params']

		if(action_type == LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE):
			mirek = params['mirek']
			for light in self.lights:
				light.set_color_temperature(mirek)

		if(action_type == LightActionType.ALL_LIGHTS_SET_BRIGHTNESS):
			brightness = params['brightness']
			for light in self.lights:
				light.set_brightness(brightness)

		if(action_type == LightActionType.ALL_LIGHTS_SET_COLOR_XY):
			pass

		if(action_type == LightActionType.ALL_LIGHTS_FLASH_COLOR):
			pass




		# if(action_type == LightActionType.ALL):
		# 	pass

