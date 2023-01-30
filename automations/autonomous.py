import utils.time_utilities

# Determines if and when autonomous schedules(based on saved preferences) should be built 

class AutonomousController():
    
    def __init__(self, master_controller) -> None:
        self.master_controller = master_controller
        self.circadian_controller = master_controller.circadian_lights_controller


    def run(self):

        # Circadian lights schedule should be be built every day at midnight 
        if(is_midnight()):
            circadian_lights_controller.build()

