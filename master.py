from automations.pyhue.bridge import BridgeController
# from automations.circadian import CircadianLightsController
from automations.weather import WeatherController
import time

class MasterController():
	
	# Maybe make this more complete later, right now I just need a timer
	# In the future, a dedicated thread for a terminal deamon I can open and close and send commands to

	def __init__(self):
		# self.schedule = None
		self.weather_controller = WeatherController(self)
		# self.circadian_lights_controller = CircadianLightsController(self)
		self.bridge_controller = BridgeController(self)
		# self.circadian_lights_controller.generate_schedule()
		# self.main_loop()

		for light in self.bridge_controller.lights:
			# light.setDuration(10000)
			light.turn_on()
			response = light.set_color_temperature(100)
			light.set_brightness(100)

		# 	print(response)


	def main_loop(self):
		self.circadian_lights.tick()
		

master_controller = MasterController()