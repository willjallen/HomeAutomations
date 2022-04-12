from automations.pyhue.bridge import BridgeController

import automations.constants
from automations.schedule import Schedule
import automations.weather
import utils.time_utilities as time_utils

import datetime
# Every day at some time, find the sunset and sunrise time from an api, write it to a file
# Then every 10 minutes send a request to the hue lights to fade colors
# From very blue and bright to orange and dark - mirroring the natural light from outdoors

# However, I want some control over this

# For exmaple if sunrise is at 8 am and sets at 7 pm
# I don't really want all the lights to turn off at 7 pm, so I should be able to add some length to the tails



	
class CircadianLightsController():
	def __init__(self, master_controller):
		
		self.master_controller = master_controller
		self.weather_controller = master_controller.weather_controller

		self.sunrinse_time = None
		self.sunset_time = None

		# Schedule
		self.schedule = Schedule()





	def update_lights(self, **kwargs):
		pass

	# Generate a set of commands to fade the lights according to the sunset and sunrise times
	#https://brandon-lighting.com/wp-content/uploads/2018/04/Color-Temperature.jpg
	# mirek: (integer – minimum: 153(blue) – maximum: 500(red))
	# sunrise: mirek: 450, brightness: 0
	# post sunrise: mirek: 400, brightness: 100 (t+15 min)
	# early morning: mirek: 300, (noon-sunrise)/2 
	# noon: mirek: 250 (sunset - sunrise)/2
	# mid afternoon
	# sunset
	# post sunset(red)

	# Early morning
	def generate_schedule(self):

		# Update sunset and sunrise times 
		local_time = time_utils.get_local_time()
		YMD_str = str(local_time.year) + '-' + str(local_time.month) + '-' + str(local_time.day)

		self.weather_controller.retrieve_astronomy()
		
		# In UTC seconds
		self.sunrinse_time = time_utils.convert_local_time_hm_to_UTC(YMD_str + ' '  + 
			self.weather_controller.astronomy_json['sunrise']).timestamp()
		
		# In UTC seconds
		self.sunset_time = time_utils.convert_local_time_hm_to_UTC(YMD_str + ' '  + 
			self.weather_controller.astronomy_json['sunset']).timestamp()



		self.noon_time = sunrinse_time + (sunset_time - sunrinse_time)/2

		# 

		# print(self.weather_controller.astronomy_json['sunrise'])
		# print(self.sunrinse_time)
		# print(self.sunrinse_time.timestamp())
		# print(time_utils.get_UTC())
		# print(time_utils.get_UTC().timestamp())


	def tick(self, curr_time):
		soonest_item = self.schedule.get_soonest_item()
		if(curr_time - soonest_item.execution_time >= 0 and not soonest_item.executed):
			
			if(soonest_item.action_type == CircadianActionTypes.GENERATE_SCHEDULE):
				generate_schedule()

			if(soonest_item.action_type == CircadianActionTypes.UPDATE_LIGHTS):
				update_lights(soonest_item.params)


