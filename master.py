from automations.pyhue.bridge import BridgeController
from automations.circadian import CircadianLightsController
from automations.weather import WeatherController
from automations.autonomous import AutonomousController
from automations.pyhue.color import Color
from automations.constants import ColorType
import utils.time_utilities as time_utils
import threading
import time

class MasterController():


    def __init__(self):
        # self.schedule = Schedule()


        self.weather_controller = WeatherController(self)
        self.circadian_lights_controller = CircadianLightsController(self)
        self.bridge_controller = BridgeController(self)
        self.circadian_lights_controller.generate_schedule()

        self.autonomous_controller = AutonomousController(self)



        # self.console_thread =
        # self.autonomous_thread = threading.Thread(target=)

        # self.event_loop = asyncio.new_event_loop()



        red = (0.6882, 0.3108)
        blue = (0.1532, 0.0495)
        orig = Color(ColorType.XY, x=red[0], y=red[1])
        new = Color(ColorType.XY, x=blue[0], y=blue[1])
        for light in self.bridge_controller.lights:
            light.flash_color(orig, new, 5000)

        f = open("schedule.txt", "a")

        for item in self.circadian_lights_controller.schedule.items:
            f.write(str(item) + '\n\n')

        f.close()

        self.main_loop()


        # for light in self.bridge_controller.lights:
        #       light.setDuration(10000)
        #       light.turn_on()
        #       color = Color(ColorType.TEMPERATURE, mirek=200)
        #       response = light.set_color(color)
        #       light.set_brightness(100)

        #       print(response)lj


    def main_loop(self):
        curr_time = time_utils.get_UTC_time().timestamp()
        midnight_tomorrow = time_utils.get_tomorrow_start_as_utc().timestamp()
        print(time_utils.get_local_time())
        print(time_utils.get_local_tomorrow_start())
        print(time_utils.get_UTC_time())
        print(time_utils.get_tomorrow_start_as_utc())
        while(True):
            curr_time = time_utils.get_UTC_time().timestamp()
            if(curr_time < midnight_tomorrow): # This needs to become a schedule item
                self.circadian_lights_controller.tick(curr_time)
            #
            # if(len(self.schedule.items) != 0):
            #     item = self.schedule.get_next_item()
            #     if(curr_time - item.execution_time >= 0 and not item.executed):
            #         # print('Executing item: ' + str(item))
            #         self.master_controller.bridge_controller.update_lights(action_type=item.action_type, params=item.params)
            #         self.schedule.remove_item(item)

            else:
                self.circadian_lights_controller.generate_schedule()
                midnight_tomorrow = time_utils.get_tomorrow_start_as_utc().timestamp()




master_controller = MasterController()
