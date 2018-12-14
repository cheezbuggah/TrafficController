from Scripts.controller.controller import Controller
from Scripts.controller.controller import Algorithm
import random


class Randomizer(Algorithm):
	def __init__(self):
		super().__init__()
		self.counter = 0

	def calculate_new_floor_plan(self):
		# Count to 33 as to end up with about 5 seconds.
		if self.counter < 33:
			self.counter += 1
			return
		else:
			self.counter = 0

		modified_light_code = random.choice(list(self.controller.floorPlan.keys()))

		for light in Controller.ALL_KNOWN_TRAFFIC_LIGHTS:
			colour = self.controller.floorPlan[light]['colour']

			if colour == Controller.LIGHT_COLOR_GREEN or colour == Controller.LIGHT_COLOR_ORANGE:
				modified_light_code = light

		modified_light = self.controller.floorPlan[modified_light_code]

		if modified_light['colour'] == Controller.LIGHT_COLOR_RED:
			self.controller.floorPlan[modified_light_code]['colour'] = Controller.LIGHT_COLOR_GREEN
		elif modified_light['colour'] == Controller.LIGHT_COLOR_ORANGE:
			self.controller.floorPlan[modified_light_code]['colour'] = Controller.LIGHT_COLOR_RED
		else:
			self.controller.floorPlan[modified_light_code]['colour'] = Controller.LIGHT_COLOR_ORANGE

	def __str__(self):
		return 'Randomizer'