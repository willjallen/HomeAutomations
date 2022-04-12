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

second = 1
minute = 60
hour = 60*minute

	
class CircadianLightsController():
	def __init__(self, master_controller):
		
		self.master_controller = master_controller
		self.weather_controller = master_controller.weather_controller

		self.sunrinse_time = None
		self.sunset_time = None

		# Schedule
		self.schedule = Schedule()

		self.sleep_time = 8.5 * hour
		self.wind_down_time = 45 * minute



	def update_lights(self, **kwargs):
		pass

	# Generate a set of commands to fade the lights according to the sunset and sunrise times
	#https://brandon-lighting.com/wp-content/uploads/2018/04/Color-Temperature.jpg
	# mirek: (integer – minimum: 153(blue) – maximum: 500(red))
	# sunrise: mirek: 450, brightness: 1
	# post sunrise: mirek: 400, brightness: 100 (t+15 min)
	# early morning: mirek: 300, brightness: 100 (t+30 min) 
	# midday: mirek: 250 (sunset - sunrise)/2
	# mid afternoon: mirek: 300, brightness: 100 (sunset-midday)/2
	# sunset: mirek: 450, brightness: 80
	# post sunset: mirek: 500, brightness: 70 (t+30 min) 
	# night(red): red, brightness: 70 (11:59 pm - (hours_of_sleep - sunrise)) - 45 min
	# sleep indicator sleep(flash blue, then red) (t+15 min) brightness: 60
	# sleep indicator sleep(flash blue, then red) (t+15 min) brightness: 40
	# sleep indicator sleep(flash blue, then red) (t+15 min) brightness: 20

	# Early morning
	def generate_schedule(self):

		# Update sunset and sunrise times 
		local_time = time_utils.get_local_time()
		YMD_str = str(local_time.year) + '-' + str(local_time.month) + '-' + str(local_time.day)

		# self.weather_controller.retrieve_astronomy()
		
		# In UTC seconds
		sunrinse_time = time_utils.convert_local_time_hm_to_UTC(YMD_str + ' '  + 
			self.weather_controller.astronomy_json['sunrise']).timestamp()
		
		# In UTC seconds
		sunset_time = time_utils.convert_local_time_hm_to_UTC(YMD_str + ' '  + 
			self.weather_controller.astronomy_json['sunset']).timestamp()

		print(sunrinse_time)
		print(sunset_time)

		midday_time = sunrinse_time + (sunset_time - sunrinse_time)/2


		post_sunrise_time = sunrinse_time + (15 * minute)
		
		early_morning_time = sunrinse_time + (midday_time - sunrinse_time)/2

		mid_afternoon_time = midday_time + (sunset_time - midday_time)/2

		post_sunset_time = sunset_time + (minute * 30)

		# tomorrow's sunrise (today's sunrise + 24 hour)
		# - sleep_time hour - 45 min
		#
		night_time = (sunrinse_time + (24 * hour)) - self.sleep_time - self.wind_down_time
		
		first_sleep_indicator_time = night_time + (self.wind_down_time/3)

		second_sleep_indicator_time = first_sleep_indicator_time + (self.wind_down_time/3)

		third_sleep_indicator_time = second_sleep_indicator_time + (self.wind_down_time/3)

		lights_out = third_sleep_indicator_time + (5 * minute)

		print('Sunrise: ' + (time_utils.UTC_timestamp_to_local_datetime(sunrinse_time)).strftime('%I:%M %p'))
		print('Post sunrise: ' + (time_utils.UTC_timestamp_to_local_datetime(post_sunrise_time)).strftime('%I:%M %p'))
		print('Early morning: ' + (time_utils.UTC_timestamp_to_local_datetime(early_morning_time)).strftime('%I:%M %p'))
		print('Mid day: ' + (time_utils.UTC_timestamp_to_local_datetime(midday_time)).strftime('%I:%M %p'))
		print('Mid afternoon: ' + (time_utils.UTC_timestamp_to_local_datetime(mid_afternoon_time)).strftime('%I:%M %p'))
		print('Sunset: ' + (time_utils.UTC_timestamp_to_local_datetime(sunset_time)).strftime('%I:%M %p'))
		print('Post sunset: ' + (time_utils.UTC_timestamp_to_local_datetime(post_sunset_time)).strftime('%I:%M %p'))
		print('Nighttime: ' + (time_utils.UTC_timestamp_to_local_datetime(night_time)).strftime('%I:%M %p'))
		print('First sleep ind.: ' + (time_utils.UTC_timestamp_to_local_datetime(first_sleep_indicator_time)).strftime('%I:%M %p'))
		print('Second sleep indc.: ' + (time_utils.UTC_timestamp_to_local_datetime(second_sleep_indicator_time)).strftime('%I:%M %p'))
		print('Third sleep indc.: ' + (time_utils.UTC_timestamp_to_local_datetime(third_sleep_indicator_time)).strftime('%I:%M %p'))
		print('Lights out: ' + (time_utils.UTC_timestamp_to_local_datetime(lights_out)).strftime('%I:%M %p'))
		# 

		# print(self.weather_controller.astronomy_json['sunrise'])
		# print(self.sunrinse_time)
		# print(self.sunrinse_time.timestamp())
		# print(time_utils.get_UTC())
		# print(time_utils.get_UTC().timestamp())


	def tick(self):
		next_item = self.schedule.get_next_item()
		if(time_utils.get_UTC_time() - next_item.execution_time >= 0 and not next_item.executed):
			
			if(next_item.action_type == CircadianActionTypes.GENERATE_SCHEDULE):
				generate_schedule()

			if(next_item.action_type == CircadianActionTypes.UPDATE_LIGHTS):
				update_lights(next_item.params)


