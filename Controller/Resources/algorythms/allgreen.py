from Scripts.controller.controller import Controller
from Scripts.controller.controller import Algorithm


class AllGreen(Algorithm):

	def calculate_new_floor_plan(self):
		colours = [
			Controller.LIGHT_COLOR_GREEN
		]

		for light in Controller.ALL_KNOWN_TRAFFIC_LIGHTS:
			self.controller.floorPlan[light] = {
				'colour': colours,
				'timer': 2,
				'hasTraffic': False
			}

	def __str__(self):
		return 'AllGreen'
