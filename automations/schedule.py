





class Item():
	# execution_time: UTC time on which the item should be executed
	# automation_type: 
	# action_type: which action the controller will take
	# params: dictionary enumerated parameters for action
	def __init__(self, execution_time, automation_type, action_type, params):
		self.execution_time = execution_time
		self.automation_type = automation_type
		self.action_type = action_type
		self.params = params

		self.executed = False

class Schedule():
	def __init__(self):
		self.items = []

	def add_item(self, item):
		self.items.append(item)

	def get_soonest_item(self, curr_time):
		min_delta = sys.maxsize
		soonest_item = None
		for item in items:
			if(abs(curr_time - item.execution_time) < min_delta):
				soonest_item = item
				min_delta = abs(curr_time - item.execution_time)
		return soonest_item


	def get_all_items(self):
		return self.items

	def remove_all_items(self):
		self.items = []