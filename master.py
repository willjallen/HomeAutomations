from automations.pyhue.bridge import BridgeController
from automations.circadian import CircadianLightsController
from automations.weather import WeatherController
import time
from automations.pyhue.color import Color
from automations.constants import ColorType
import utils.time_utilities as time_utils
class MasterController():
	
	# Maybe make this more complete later, right now I just need a timer
	# In the future, a dedicated thread for a terminal deamon I can open and close and send commands to

	def __init__(self):
		# self.schedule = None
		self.weather_controller = WeatherController(self)
		self.circadian_lights_controller = CircadianLightsController(self)
		self.bridge_controller = BridgeController(self)
		self.circadian_lights_controller.generate_schedule()
		red = (0.6882, 0.3108)
		blue = (0.1532, 0.0495) 
		orig = Color(ColorType.XY, x=red[0], y=red[1])
		new = Color(ColorType.XY, x=blue[0], y=blue[1])
		for light in self.bridge_controller.lights:
			light.flash_color(orig, new, 5000)

		f = open("schedule.txt", "a")
	
		for item in self.circadian_lights_controller.light_schedule.items:
			f.write(str(item) + '\n\n')
	
		f.close()

		self.main_loop()


		# for light in self.bridge_controller.lights:
		# 	light.setDuration(10000)
		# 	light.turn_on()
		# 	color = Color(ColorType.TEMPERATURE, mirek=200)
		# 	response = light.set_color(color)
		# 	light.set_brightness(100)

		# 	print(response)lj


	def main_loop(self):
		curr_time = time_utils.get_UTC_time().timestamp()
		midnight_tomorrow = time_utils.get_tomorrow_start_as_utc().timestamp()
		print(time_utils.get_local_time())
		print(time_utils.get_local_tomorrow_start())
		print(time_utils.get_UTC_time())
		print(time_utils.get_tomorrow_start_as_utc())
		while(True):
			curr_time = time_utils.get_UTC_time().timestamp()
			if(curr_time < midnight_tomorrow):
				self.circadian_lights_controller.tick(curr_time)
			else:
				self.circadian_lights_controller.generate_schedule()
				midnight_tomorrow = time_utils.get_tomorrow_start_as_utc().timestamp()


master_controller = MasterController()


	








