# import automations.pyhue.environment as env
import json
import automations.pyhue.patched_request as prequests
import requests as requests
import environment as env
from automations.pyhue.light import Light
from automations.constants import LightActionType



def get_bridge_id():
	pass



class BridgeController():
	def __init__(self, master_controller):
		self.master_controller = master_controller
		self.lights = []
		self.retrieve_lights_data()
		

	def get_lights(self):
		return self.lights


	def retrieve_lights_data(self):

		response = prequests.get(url=env.url + '/light')
		
		lightsData = response.json()['data']

		self.numLights = len(lightsData)
		# print(json.dumps(lightsData, indent=4))
		for i in range(0, len(lightsData)):
			light = Light(bridge=self, data=lightsData[i])
			if(i >= len(self.lights)):
				self.lights.append(light)	
			else:
				self.lights[i] = light  


	def update_light(self, **kwargs):
		pass


	def update_lights(self, action_type, params):
		
		if(action_type == LightActionType.ALL_LIGHTS_TURN_ON):
			for light in self.lights:
				light.turn_on()

		if(action_type == LightActionType.ALL_LIGHTS_TURN_OFF):
			for light in self.lights:
				light.turn_off()


		if(action_type == LightActionType.ALL_LIGHTS_SET_COLOR):
			color = params['color']
			for light in self.lights:
				light.set_color(color)

		if(action_type == LightActionType.ALL_LIGHTS_SET_BRIGHTNESS):
			brightness = params['brightness']
			for light in self.lights:
				light.set_brightness(brightness)

		if(action_type == LightActionType.ALL_LIGHTS_FLASH_COLOR):
			original_color = params['original_color']
			color = params['color']
			duration = params['duration']
			for light in self.lights:
				light.flash_color(original_color, color, duration)




		# if(action_type == LightActionType.ALL):
		# 	pass

