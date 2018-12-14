from Scripts.controller.controller import Controller
from Scripts.controller.controller import Algorithm


class ZondagsRust(Algorithm):
	def calculate_new_floor_plan(self):
		for light in Controller.ALL_KNOWN_TRAFFIC_LIGHTS:
			self.controller.floorPlan[light] = {
				'colour': Controller.LIGHT_COLOR_ORANGE,
				'timer': -1,
				'hasTraffic': False
			}

	def __str__( self ):
		return 'ZondagsRust'
