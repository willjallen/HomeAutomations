from automations import circadian

import time

class MasterController():
	
	# Maybe make this more complete later, right now I just need a timer
	# In the future, a dedicated thread for a terminal deamon I can open and close and send commands to

	def __init__(self):
		# self.schedule = None
		self.circadian_lights = CircadianLightsController()
		self.main_loop()


	def main_loop(self):
		self.circadian_lights.tick()
		

master_controller = MasterController()