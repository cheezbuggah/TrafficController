import random
from typing import Dict
from typing import List
from Scripts.controller.controller import Algorithm
from Scripts.controller.controller import Controller


class Heuristic(Algorithm):
	light_map: Dict[str, List[str]] = {
		  'A1': ['A5', 'A7', 'B1', 'C1.1', 'C3.2', 'D1'],
		  'A2': ['A5', 'A7', 'A8', 'A9', 'A10', 'B1', 'C1.1', 'D1', 'E1'],
		  'A3': ['A5', 'A6', 'A7', 'A9', 'A10', 'B1', 'B2', 'C1.1', 'C2.2', 'D1'],
		  'A4': ['A6', 'A10', 'B1', 'B2', 'C2.1', 'C1.2', 'D1'],
		  'A5': ['A1', 'A2', 'A3', 'A6', 'A7', 'A10', 'B1', 'B3', 'C2.1', 'C3.2', 'D1'],
		  'A6': ['A3', 'A4', 'A5', 'A9', 'A10', 'B1', 'B2', 'C1.2', 'C2.2', 'D1', 'E1'],
		  'A7': ['A1', 'A2', 'A3', 'A5', 'A9', 'A10', 'B3', 'C3.2', 'D1', 'E1'],
		  'A8': ['A2', 'A7', 'B3', 'C3.1', 'E1'],
		  'A9': ['A2', 'A3', 'A6', 'A7', 'B2', 'B3', 'C2.2', 'C3.1'],
		 'A10': ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'B2', 'B3', 'C1.2', 'C3.2', 'D1'],
		  'B1': ['A1', 'A2', 'A3', 'A4', 'A6', 'A10'],
		  'B2': ['A3', 'A4', 'A5', 'A6', 'A9', 'D1'],
		  'B3': ['A1', 'A5', 'A7', 'A8', 'A9', 'A10', 'D1'],
		'C1.1': ['A1', 'A2', 'A3'],
		'C1.2': ['A4', 'A6', 'A10'],
		'C2.1': ['A4', 'A5', 'D1'],
		'C2.2': ['A3', 'A6', 'A9'],
		'C3.1': ['A8', 'A9', 'A10'],
		'C3.2': ['A1', 'A5', 'A7', 'D1'],
		  'D1': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A10', 'B2', 'B3', 'C2.1', 'C3.2'],
		  # Included for ease of use, but beware that the train does not stop for these lanes!
		  'E1': ['A2', 'A6', 'A7', 'A8'],
		  'F1': ['A2', 'A6', 'A7', 'A8'],
		  'F2': ['A2', 'A6', 'A7', 'A8']
	}

	red: str = Controller.red_light
	orange: str = Controller.orange_light
	green: str = Controller.green_light

	def __init__(self):
		super().__init__()

		# E1, F1 & F2 are last in the list, but shouldn't be managed by the controller.
		# They should only be called on when the simulator signals for an approaching train. Hence the removal
		# of the last 3 elements in the light map.
		self.lightEvaluationOrder: List[str] = list(self.light_map.keys())[:-3]

	# method to set all crossing lanes to red
	def cross_stop(self, light: str):
		"""
		Set all lanes that cross a specific lane to orange, where it will be picked up by the loop and set to red
		:param light: traffic light code
		:type light: str
		"""
		for laneLight in self.light_map[light]:
			if self.controller.floorPlan[laneLight]['colour'] == self.green:
				self.set_light(laneLight, self.orange, duration=self.orange_duration(laneLight))

	def set_light(self, light: str, colour: str, duration=None):
		"""
		Set a specific light to a specific colour.
		This also reset the timer for that light back to 0.

		:param duration: the colour time received from the simulator
		:param light: traffic light code
		:type light: str
		:param colour: traffic light colour
		:type colour: str
		"""
		self.controller.floorPlan[light]['colour'] = colour
		self.controller.floorPlan[light]['ticks'] = 0
		self.controller.floorPlan[light]['timer'] = duration

	def check_path_free(self, light: str) -> bool:
		"""
		Determines if the paths crossing a specific light are not currently in use (set to red).

		:param light: traffic light code
		:type light: str
		:return: If the traffic lights of the crossing paths are red
		:rtype bool
		"""
		for blocker in self.light_map[light]:
			if self.controller.floorPlan[blocker]['colour'] != self.red:
				return False
		return True

	def orange_duration(self, light: str) -> int:
		"""
		Determines the duration (in ticks) the given light should remain orange.

		:param light: traffic light code for which to determine the duration
		:type light: str
		:return: Amount of ticks the given light should be orange
		:rtype int
		"""
		group = light[0]
		if group == 'F':
			group = 'E'

		durations = {
			'A': 4,  # 4 seconds
			'B': 2,  # 2 seconds
			'C': 2,  # 2 seconds
			'D': 4,  # 4 seconds
			'E': 2  # 2 seconds
		}

		return durations[group]

	def green_duration(self, light: str) -> int:
		"""
		Determines the duration (in ticks) the given light should remain green.

		:param light: traffic light code for which to determine the duration
		:type light: str
		:return: Amount of ticks the given light should be green
		:rtype int
		"""
		group = light[0]
		if group == 'F':
			group = 'E'

		durations = {
			'A': 7,  # 7 seconds
			'B': 7,  # 7 seconds
			'C': 5,  # 5 seconds
			'D': 4,  # 4 seconds
			'E': 30  # 30 seconds
		}

		return durations[group]

	def random_green_time(self, light: str) -> int:
		"""
		Determines the duration (in ticks) after which the given light should go green.
		This is mainly here to assist simulators that have trouble letting know if traffic is waiting.

		:param light: traffic light code for which to determine the duration
		:type light: str
		:return: Amount of ticks
		:rtype int
		"""
		group = light[0]
		if group == 'F':
			group = 'E'

		durations = {
			'A': 60,  # 60 seconds
			'B': 100,  # 100 seconds
			'C': 120,  # 120 seconds
			'D': -1,  # Not supported
			'E': -1  # Not supported
		}

		return durations[group]

	def calculate_new_floor_plan(self):
		# Do some simple stuff, like:
		## Turn an orange light red when it has been orange for the duration the specific light should stay orange.
		## Turn a green light orange when it has been green for the duration the specific light should stay green.
		for light, info in self.controller.floorPlan.items():
			info['ticks'] += 1

			orange_duration = self.orange_duration(light)
			green_duration = self.green_duration(light)

			if info['colour'] == self.orange and info['ticks'] > orange_duration:
				self.set_light(light, self.red)
				if light == 'E1':
					self.set_light('F1', self.red, duration=None)
					self.set_light('F2', self.red, duration=None)

			elif info['colour'] == self.green and info['ticks'] > green_duration:
				self.set_light(light, self.orange, duration=self.orange_duration(light))
				# Set hasTraffic to false now, so that any report of new traffic will be caught during the orange state.
				info['hasTraffic'] = False
				if light == 'E1':
					if self.controller.floorPlan['F1']['hasTraffic']:
						self.set_light('F1', self.orange, duration=self.orange_duration('F1'))
						self.controller.floorPlan['F1']['hasTraffic'] = False
					if self.controller.floorPlan['F2']['hasTraffic']:
						self.set_light('F2', self.orange, duration=self.orange_duration('F2'))
						self.controller.floorPlan['F2']['hasTraffic'] = False

		if self.controller.floorPlan['D1']['hasTraffic'] and self.controller.floorPlan['D1']['colour'] == self.red:
			if not self.check_path_free('D1'):
				if self.controller.floorPlan['D1']['ticks'] > 15:
					self.cross_stop('D1')
			else:
				self.set_light('D1', self.green, duration=self.green_duration('D1'))

		# Trains don't stop. Ensure all lights that route to the intersection will be red when the train passes.
		if self.controller.floorPlan['E1']['hasTraffic'] and self.controller.floorPlan['E1']['colour'] == self.red:
			if not self.check_path_free('E1'):
				self.cross_stop('E1')
			else:
				if self.controller.floorPlan['F1']['hasTraffic']:
					self.set_light('F1', self.green, duration=self.green_duration('F1'))
				elif self.controller.floorPlan['F2']['hasTraffic']:
					self.set_light('F2', self.green, duration=self.green_duration('F2'))
				self.set_light('E1', self.green, duration=self.green_duration('E1'))

		#take a random light to prevent the first lights in the list to always go green first
		random.shuffle(self.lightEvaluationOrder)

		for light in self.lightEvaluationOrder:
			info = self.controller.floorPlan[light]

			if info['colour'] == self.red:
				if info['hasTraffic']:
					if self.check_path_free(light):
						self.set_light(light, self.green, duration=self.green_duration(light))
					# Set the traffic light to green if traffic has been waiting for more than a minute.
					elif info['ticks'] > 60:
						self.cross_stop(light)
				# This is mainly here to assist simulators that have trouble letting know if traffic is waiting.
				# After about 60 seconds, a light will go green when it it safe to do so.
				elif self.check_path_free(light) and info['ticks'] > self.random_green_time(light) and light != 'D1':
					self.set_light(light, self.green, duration=self.green_duration(light))



	def __str__(self) -> str:
		return 'Heuristic'
