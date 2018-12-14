from Scripts.controller.controller import Controller
from Scripts.controller.controller import Algorithm
import random


class Disco(Algorithm):

	def calculate_new_floor_plan(self):
		colours = [
			Controller.LIGHT_COLOR_RED,
			Controller.LIGHT_COLOR_ORANGE,
			Controller.LIGHT_COLOR_GREEN
		]

		for light in Controller.ALL_KNOWN_TRAFFIC_LIGHTS:
			self.controller.floorPlan[light] = {
				'colour': random.choice(colours),
				'timer': None,
				'hasTraffic': False
			}

	def __str__( self ):
		return 'Disco'
