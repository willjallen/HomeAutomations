import utils.time_utilities as time_utils





class Item():
	# execution_time: UTC time on which the item should be executed
	# automation_type: 
	# action_type: which action the controller will take
	# params: dictionary enumerated parameters for action
	def __init__(self, execution_time, action_type, params):
		self.execution_time = execution_time
		self.action_type = action_type
		self.params = params

		self.executed = False

	def __str__(self):
		if(self.params):
			if('color' in self.params.keys() and 'original_color' in self.params.keys()):
				return_str = 'time: ' + str(time_utils.UTC_timestamp_to_local_datetime(self.execution_time).strftime('%I:%M %p')) + '\n' +'action type: ' + str(self.action_type) + '\n' + 'params: ' + str(self.params['color']) + ', ' + str(self.params['original_color']) 
			elif('color' in self.params.keys()):
				return_str = 'time: ' + str(time_utils.UTC_timestamp_to_local_datetime(self.execution_time).strftime('%I:%M %p')) + '\n' +'action type: ' + str(self.action_type) + '\n' + 'params: ' + str(self.params['color'])
			elif('brightness' in self.params.keys()):
				return_str = 'time: ' + str(time_utils.UTC_timestamp_to_local_datetime(self.execution_time).strftime('%I:%M %p')) + '\n' +'action type: ' + str(self.action_type) + '\n' + 'params: ' + str(self.params['brightness'])

		else:
			return_str = 'time: ' + str(time_utils.UTC_timestamp_to_local_datetime(self.execution_time).strftime('%I:%M %p')) + '\n' +'action type: ' + str(self.action_type) + '\n' + 'params: None'

		return return_str

class Schedule():
	def __init__(self):
		self.items = []
		self.build_time = time_utils.get_UTC_time().timestamp()

	def add_item(self, item):
		if(item.execution_time >= self.build_time):
			# print(str(time_utils.UTC_timestamp_to_local_datetime(item.execution_time).strftime('%I:%M %p')))
			self.items.append(item)
			self.items.sort(key=lambda x: x.execution_time)

	# def get_soonest_item(self, curr_time):
	# 	min_delta = sys.maxsize
	# 	soonest_item = None
	# 	for item in items:
	# 		if(abs(curr_time - item.execution_time) < min_delta):
	# 			soonest_item = item
	# 			min_delta = abs(curr_time - item.execution_time)
	# 	return soonest_item

	def set_build_time(self, build_time):
		self.build_time = build_time

	def remove_item(self, item):
		self.items.remove(item)

	def get_next_item(self):
		return self.items[0]

	def get_all_items(self):
		return self.items

	def clear(self):
		self.items = []