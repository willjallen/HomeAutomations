from pyhue import bridge

import constants
import schedule
import weather
import time_utilities
# Every day at some time, find the sunset and sunrise time from an api, write it to a file
# Then every 10 minutes send a request to the hue lights to fade colors
# From very blue and bright to orange and dark - mirroring the natural light from outdoors

# However, I want some control over this

# For exmaple if sunrise is at 8 am and sets at 7 pm
# I don't really want all the lights to turn off at 7 pm, so I should be able to add some length to the tails



	
class CircadianLightsController():
	def __init__(self):
		
		self.sunrinse_time = None
		self.sunset_time = None

		# Schedule
		self.schedule = Schedule()





	def update_lights(self, **kwargs):
		pass

	# Generate a set of commands to fade the lights according to the sunset and sunrise times
	def generate_schedule(self):
		# Update sunset and sunrise times 
		weather.retrieve_astronomy()
		self.sunrinse_time = time_utilities.convert_local_time_hm_to_UTC(weather.astronomy_json['sunrise'])
		self.sunset_time = time_utilities.convert_local_time_hm_to_UTC(weather.astronomy_json['sunset'])

		pass

	def tick(self, curr_time):
		soonest_item = self.schedule.get_soonest_item()
		if(curr_time - soonest_item.execution_time >= 0 and not soonest_item.executed):
			
			elif(soonest_item.action_type == CircadianActionTypes.GENERATE_SCHEDULE):
				generate_schedule()

			if(soonest_item.action_type == CircadianActionTypes.UPDATE_LIGHTS):
				update_lights(soonest_item.params)


