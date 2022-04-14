from enum import Enum
import uuid

class ActionType(Enum):
	LIGHT = uuid.uuid4()
	BLINDS = uuid.uuid4()
	CIRCADIAN = uuid.uuid4()

class CircadianActionType(Enum):
	GENERATE_SCHEDULE = uuid.uuid4()

class LightActionType(Enum):

	ALL_LIGHTS_TURN_OFF = uuid.uuid4()
	ALL_LIGHTS_TURN_ON = uuid.uuid4()

	ALL_LIGHTS_SET_BRIGHTNESS = uuid.uuid4()

	ALL_LIGHTS_SET_COLOR_TEMPERATURE = uuid.uuid4()
	ALL_LIGHTS_SET_COLOR_XY = uuid.uuid4()
	ALL_LIGHTS_SET_COLOR_RGB = uuid.uuid4()

	ALL_LIGHTS_FLASH_COLOR = uuid.uuid4()


	LIGHT_SET_BRIGHTNESS = uuid.uuid4()
	LIGHT_SET_COLOR_TEMPERATURE = uuid.uuid4()

class BlindActionType(Enum):
	something = 354354