from automations.pyhue.bridge import BridgeController
from automations.pyhue.color import Color

from automations.constants import ColorType
from automations.constants import LightActionType
import automations.weather
import automations.constants
from automations.schedule import Schedule
from automations.schedule import Item

import utils.time_utilities as time_utils
import datetime


# Every day at some time, find the sunset and sunrise time from an api, write it to a file
# Then every 10 minutes send a request to the hue lights to fade colors
# From very blue and bright to orange and dark - mirroring the natural light from outdoors

# However, I want some control over this

# For exmaple if sunrise is at 8 am and sets at 7 pm
# I don't really want all the lights to turn off at 7 pm, so I should be able to add some length to the tails

milliseconds = 1000
second = 1
minute = 60
hour = 60*minute

# in XY
red = (0.6882, 0.3108)
blue = (0.1532, 0.0495) 

class CircadianLightsController():
	def __init__(self, master_controller):
		
		self.master_controller = master_controller
		self.weather_controller = master_controller.weather_controller

		self.sunrinse_time = None
		self.sunset_time = None

		# Schedule
		self.schedule = Schedule()

		# Sunrise is at 6:30 AM, but I want to wake up at 8:30 AM
		# in hours
		self.sunrise_delay = 0

		self.update_interval = 1 * minute 


		self.sleep_time = 8.5 * hour
		self.wind_down_time = 45 * minute

		self.sunrise_mirek = 450
		self.sunrise_brightness = 1

		self.post_sunrise_mirek = 400
		self.post_sunrise_brightness = 100

		self.early_morning_mirek = 300
		self.early_morning_brightness = 100

		self.midday_mirek = 250
		self.midday_brightness = 100	

		self.mid_afternoon_mirek = 300
		self.mid_afternoon_brightness = 100

		self.sunset_mirek = 450
		self.sunset_brightness = 80

		self.post_sunset_mirek = 500
		self.post_sunset_brightness = 70

		self.night_color = Color(ColorType.XY, x=red[0], y=red[1])
		self.night_brightness = 60

		self.first_sleep_indicator_color = Color(ColorType.XY, x=blue[0], y=blue[1])
		# in ms
		self.first_sleep_indicator_flash_duration = 1 * second * milliseconds


		self.second_sleep_indicator_color = Color(ColorType.XY, x=blue[0], y=blue[1])
		# in ms
		self.second_sleep_indicator_flash_duration = 1 * second * milliseconds


		self.third_sleep_indicator_color = Color(ColorType.XY, x=blue[0], y=blue[1])
		# in ms
		self.third_sleep_indicator_flash_duration = 1 * second * milliseconds
		self.lights_out_brightness = 30



	# def update_lights(self, **kwargs):
	
	# 		self.master_controller.bridge_controller.set

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

		local_time = time_utils.get_local_time()
		YMD_str = str(local_time.year) + '-' + str(local_time.month) + '-' + str(local_time.day)

		self.weather_controller.retrieve_astronomy()
		
		# Update sunset and sunrise times 
		# In UTC seconds
		sunrise_time_without_delay = time_utils.convert_local_time_hm_to_UTC(YMD_str + ' '  + 
			self.weather_controller.astronomy_json['sunrise']).timestamp()

		sunrinse_time = sunrise_time_without_delay + (self.sunrise_delay * hour)
		

		lights_on_time = sunrinse_time - (5 * second)

		# In UTC seconds
		sunset_time = time_utils.convert_local_time_hm_to_UTC(YMD_str + ' '  + 
			self.weather_controller.astronomy_json['sunset']).timestamp()

		print(sunrinse_time)
		print(sunset_time)

		midday_time = sunrinse_time + (sunset_time - sunrinse_time)/2


		post_sunrise_time = sunrinse_time + (15 * minute)
		
		early_morning_time = sunrinse_time + (midday_time - sunrinse_time)/2

		mid_afternoon_time = midday_time + (sunset_time - midday_time)/2

		post_sunset_time = sunset_time + (minute * 60)

		# tomorrow's sunrise (today's sunrise + 24 hour)
		# - sleep_time hour - 45 min
		#
		night_time = (sunrinse_time + (24 * hour)) - self.sleep_time - self.wind_down_time
		
		first_sleep_indicator_time = night_time + (self.wind_down_time/3)

		second_sleep_indicator_time = first_sleep_indicator_time + (self.wind_down_time/3)

		third_sleep_indicator_time = second_sleep_indicator_time + (self.wind_down_time/3)

		lights_off_time = third_sleep_indicator_time + (5 * minute)

		print('Sunrise: ' + (time_utils.UTC_timestamp_to_local_datetime(sunrise_time_without_delay)).strftime('%I:%M %p'))
		print('Delay: ' + str(self.sunrise_delay) + ' h')
		print('Sunrise (With Delay): ' + (time_utils.UTC_timestamp_to_local_datetime(sunrinse_time)).strftime('%I:%M %p'))
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
		print('Lights out: ' + (time_utils.UTC_timestamp_to_local_datetime(lights_off_time)).strftime('%I:%M %p'))
		
		turn_on = 4
		turn_off = 3
		# brightness assumed attribute
		mirek_change = 0
		color_change = 1
		flash = 2


		events = [{'automation_type':'circadian', 'name': 'sunrise', 'type': mirek_change, 'time': sunrinse_time, 'mirek': self.sunrise_mirek, 'brightness': self.sunrise_brightness},
				  {'automation_type':'circadian', 'name': 'post_sunrise', 'type': mirek_change, 'time': post_sunrise_time, 'mirek': self.post_sunrise_mirek, 'brightness': self.post_sunrise_brightness},
				  {'automation_type':'circadian', 'name': 'early_morning', 'type': mirek_change, 'time': early_morning_time, 'mirek': self.early_morning_mirek, 'brightness': self.early_morning_brightness},
				  {'automation_type':'circadian', 'name': 'midday', 'type': mirek_change, 'time': midday_time, 'mirek': self.midday_mirek, 'brightness': self.midday_brightness},
				  {'automation_type':'circadian', 'name': 'mid_afternoon', 'type': mirek_change, 'time': mid_afternoon_time, 'mirek': self.mid_afternoon_mirek, 'brightness': self.mid_afternoon_brightness},
				  {'automation_type':'circadian', 'name': 'sunset', 'type': mirek_change, 'time': sunset_time, 'mirek': self.sunset_mirek, 'brightness': self.sunset_brightness},
				  {'automation_type':'circadian', 'name': 'post_sunset', 'type': mirek_change, 'time': post_sunset_time, 'mirek': self.post_sunset_mirek, 'brightness': self.post_sunset_brightness},
				  {'automation_type':'circadian', 'name': 'nighttime', 'type': color_change, 'time': night_time, 'color': self.night_color, 'brightness': self.night_brightness},
				  {'automation_type':'circadian', 'name': 'first_indicator', 'type': flash, 'time': first_sleep_indicator_time, 'color': self.first_sleep_indicator_color},
				  {'automation_type':'circadian', 'name': 'second_inidactor', 'type': flash, 'time': second_sleep_indicator_time, 'color': self.second_sleep_indicator_color},
				  {'automation_type':'circadian', 'name': 'third_indicator', 'type': flash, 'time': third_sleep_indicator_time, 'color': self.third_sleep_indicator_color},


		]
		
		#### Build the schedule ####
		# self.schedule.clear()
		# self.schedule.set_build_time(time_utils.get_UTC_time().timestamp())

		# Turn on the lights
		self.schedule.add_item(Item(execution_time=lights_on_time, action_type=LightActionType.ALL_LIGHTS_TURN_ON, params=None))


		curr_exec_time = sunrinse_time
		curr_mirek = self.sunrise_mirek
		curr_brightness = self.sunrise_brightness

		# Fading mechanism between mirek change types
		for i in range(0, len(events)-1):
			curr_event = events[i]

			if(curr_event['type'] != mirek_change):
				continue
			
			next_event = events[i+1]
			
			# curr_exec_time = curr_event['time']
			# curr_mirek = curr_event['mirek']
			# curr_brightness = curr_event['brightness']


			if(curr_event['type'] == mirek_change and next_event['type'] == mirek_change):
				time_diff = next_event['time'] - curr_event['time']
				mirek_diff = next_event['mirek'] - curr_event['mirek']
				brightness_diff = next_event['brightness'] - curr_event['brightness']

				num_updates = time_diff / self.update_interval 

				mirek_delta = mirek_diff / num_updates
				brightness_delta = brightness_diff / num_updates
				
				## Populate the schedule
				for i in range(0, int(num_updates)):
					
					params = {'color': Color(ColorType.TEMPERATURE, mirek=int(curr_mirek))}
					self.schedule.add_item(Item(execution_time=curr_exec_time, action_type=LightActionType.ALL_LIGHTS_SET_COLOR, params=params))
					
					params = {'brightness': curr_brightness}
					self.schedule.add_item(Item(execution_time=curr_exec_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params=params))


					curr_exec_time += self.update_interval
					curr_mirek += mirek_delta
					curr_brightness += brightness_delta 
			

		# Change to color (for nighttime)

		params = {'color': self.night_color}
		self.schedule.add_item(Item(execution_time=night_time, action_type=LightActionType.ALL_LIGHTS_SET_COLOR, params=params))
		
		params = {'brightness': self.night_brightness}
		self.schedule.add_item(Item(execution_time=night_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params=params))

		# Fade only brightness
		# From nighttime to lights out

		curr_exec_time = night_time
		curr_brightness = self.night_brightness

		time_diff = lights_off_time - night_time
		brightness_diff = self.lights_out_brightness - self.night_brightness

		num_updates = time_diff / self.update_interval

		brightness_delta = brightness_diff / num_updates

		for i in range(0, int(num_updates)):
			params = {'brightness': curr_brightness}

			self.schedule.add_item(Item(execution_time=curr_exec_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params=params))

			curr_exec_time += self.update_interval
			curr_brightness += brightness_delta 



		# Add indicators (flash)
		params = {'original_color': self.night_color, 'color': self.first_sleep_indicator_color, 'duration': 1000}
		self.schedule.add_item(Item(execution_time=first_sleep_indicator_time, action_type=LightActionType.ALL_LIGHTS_FLASH_COLOR, params=params))

		params = {'original_color': self.night_color, 'color': self.second_sleep_indicator_color, 'duration': 1000}
		self.schedule.add_item(Item(execution_time=second_sleep_indicator_time, action_type=LightActionType.ALL_LIGHTS_FLASH_COLOR, params=params))

		params = {'original_color': self.night_color, 'color': self.third_sleep_indicator_color, 'duration': 1000}
		self.schedule.add_item(Item(execution_time=third_sleep_indicator_time, action_type=LightActionType.ALL_LIGHTS_FLASH_COLOR, params=params))


		# Add lights out
		self.schedule.add_item(Item(execution_time=lights_off_time, action_type=LightActionType.ALL_LIGHTS_TURN_OFF, params=None))


	def tick(self, curr_time):
		if(len(self.schedule.items) != 0):
			item = self.schedule.get_next_item()
			if(curr_time - item.execution_time >= 0 and not item.executed):
				# print('Executing item: ' + str(item))
				self.master_controller.bridge_controller.update_lights(action_type=item.action_type, params=item.params)
				self.schedule.remove_item(item)












		# # Sunrise
		# exec_time = sunrinse_time
		# num_updates = (post_sunrise_time - sunrinse_time) % self.update_interval
		# while(num_updates > 0):
		# 	# Mirek
		# 	params = {'mirek': self.sunrise_mirek}
			
		# 	# Brightness
		# 	self.schedule.add_item(Item(execution_time=sunrise_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))
			
		# 	num_updates -= 1
		# 	exec_time += self.update_interval

		# # Post sunrise
		# exec_time = post_sunrise_time
		# num_updates = (early_morning_time - post_sunrise_time) % self.update_interval
		# while(num_updates > 0):
		# 	# Mirek
		# 	params = {'mirek': self.post_sunrise_mirek}
		# 	self.schedule.add_item(Item(execution_time=post_sunrise_time, action_type=LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE, params))
		# 	# Brightness
		# 	params = {'brightness': self.post_sunrise_brightness}
		# 	self.schedule.add_item(Item(execution_time=post_sunrise_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))

		# 	num_updates -= 1
		# 	exec_time += self.update_interval


		# # Early morning
		# exec_time = early_morning_time
		# num_updates = (midday_time - early_morning_time) % self.update_interval
		# while(num_updates > 0):
		# 	# Mirek
		# 	params = {'mirek': self.early_morning_mirek}
		# 	self.schedule.add_item(Item(execution_time=early_morning_time, action_type=LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE, params))
		# 	# Brightness
		# 	params = {'brightness': self.early_morning_brightness}
		# 	self.schedule.add_item(Item(execution_time=early_morning_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))

		# 	num_updates -= 1
		# 	exec_time += self.update_interval




		# # Midday
		# exec_time = midday_time
		# num_updates = (mid_afternoon_time - midday_time) % self.update_interval
		# while(num_updates > 0):
		# 	# Mirek
		# 	params = {'mirek': self.midday_mirek}
		# 	self.schedule.add_item(Item(execution_time=midday_time, action_type=LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE, params))
		# 	# Brightness
		# 	params = {'brightness': self.midday_brightness}
		# 	self.schedule.add_item(Item(execution_time=midday_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))

		# 	num_updates -= 1
		# 	exec_time += self.update_interval




		# # Mid afternoon
		# # Mirek
		# params = {'mirek': self.mid_afternoon_mirek}
		# self.schedule.add_item(Item(execution_time=mid_afternoon_time action_type=LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE, params))
		# # Brightness
		# params = {'brightness': self.mid_afternoon_brightness}
		# self.schedule.add_item(Item(execution_time=mid_afternoon_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))

		# # Mid afternoon
		# # Mirek
		# params = {'mirek': self.mid_afternoon_mirek}
		# self.schedule.add_item(Item(execution_time=mid_afternoon_time action_type=LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE, params))
		# # Brightness
		# params = {'brightness': self.mid_afternoon_brightness}
		# self.schedule.add_item(Item(execution_time=mid_afternoon_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))

		# # Sunset
		# # Mirek
		# params = {'mirek': self.sunset_mirek}
		# self.schedule.add_item(Item(execution_time=sunset_time action_type=LightActionType.ALL_LIGHTS_SET_COLOR_TEMPERATURE, params))
		# # Brightness
		# params = {'brightness': self.sunset_brightness}
		# self.schedule.add_item(Item(execution_time=sunset_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))

		# # Night
		# # Mirek
		# params = {'color': self.night_color}
		# self.schedule.add_item(Item(execution_time=night_time action_type=LightActionType.ALL_LIGHTS_SET_COLOR_RGB, params))
		# # Brightness
		# params = {'brightness': self.sunset_brightness}
		# self.schedule.add_item(Item(execution_time=night_time, action_type=LightActionType.ALL_LIGHTS_SET_BRIGHTNESS, params))


		# # First sleep indicator
		# params = {'color': self.first_sleep_indicator_color, 'flash_duration': self.first_sleep_indicator_flash_duration}
		# self.schedule.add_item(Item(execution_time=first_sleep_indicator_time, action_type=LightActionType.ALL_LIGHTS_FLASH_COLOR, params))

		# # Second sleep indicator
		# params = {'color': self.second_sleep_indicator_color, 'flash_duration': self.second_sleep_indicator_flash_duration}
		# self.schedule.add_item(Item(execution_time=second_sleep_indicator_time, action_type=LightActionType.ALL_LIGHTS_FLASH_COLOR, params))

		# # Third sleep indicator
		# params = {'color': self.third_sleep_indicator_color, 'flash_duration': self.third_sleep_indicator_flash_duration}
		# self.schedule.add_item(Item(execution_time=third_sleep_indicator_time, action_type=LightActionType.ALL_LIGHTS_FLASH_COLOR, params))



		# # create light

		# print(self.weather_controller.astronomy_json['sunrise'])
		# print(self.sunrinse_time)
		# print(self.sunrinse_time.timestamp())
		# print(time_utils.get_UTC())
		# print(time_utils.get_UTC().timestamp())

