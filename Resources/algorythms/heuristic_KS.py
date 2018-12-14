import random
from typing import Dict
from typing import List
from Scripts.controller.controller import Algorithm
from Scripts.controller.controller import Controller

class Heuristic( Algorithm ):
	FreeMap : Dict[str, List[str]] = {
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

	def __init__( self ):
		super().__init__()

		# E1, F1 & F2 are last in the list, but shouldn't be managed here.
		# They only should do something when the simulator flags a train as approaching.
		self.lightEvaluationOrder : List[str] = list( self.FreeMap.keys() )[:-3]

	def calculate_new_floor_plan(self):
		# Do some simple stuff, like:
		## Turn an orange light red when it has been orange for the duration the specific light should stay orange.
		## Turn a green light orange when it has been green for the duration the specific light should stay green.
		for light, info in self.controller.floorPlan.items():
			info['ticks'] += 1

			orangeDuration = self.getOrangeLightDuration( light )
			greenDuration = self.getGreenLightDuration( light )

			if info['colour'] == self.orange and info['ticks'] > orangeDuration:
				self.setLight(light, self.red)
				if light == 'E1':
					self.setLight( 'F1', self.red)
					self.setLight( 'F2', self.red)

			elif info['colour'] == self.green and info['ticks'] > greenDuration:
				self.setLight(light, self.orange)
				# Set hasTraffic to false now, so that any report of new traffic will be caught during the orange state.
				info['hasTraffic'] = False
				if light == 'E1':
					if self.controller.floorPlan['F1']['hasTraffic']:
						self.setLight( 'F1', self.orange)
						self.controller.floorPlan['F1']['hasTraffic'] = False
					if self.controller.floorPlan['F2']['hasTraffic']:
						self.setLight( 'F2', self.orange)
						self.controller.floorPlan['F2']['hasTraffic'] = False

		if self.controller.floorPlan['D1']['hasTraffic'] and self.controller.floorPlan['D1']['colour'] == self.red:
			if not self.pathIsFreeFor( 'D1' ):
				# It has been 20 seconds, people've got a train to catch!
				# Force the other traffic off the intersection and make way for the bus.
				if self.controller.floorPlan['D1']['ticks'] > 10:
					self.setCrossingLanesToRed( 'D1' )
			else:
				self.setLight( 'D1', self.green)

		# Trains don't stop. Ensure all lights that route to the intersection will be red when the train passes.
		if self.controller.floorPlan['E1']['hasTraffic'] and self.controller.floorPlan['E1']['colour'] == self.red:
			if not self.pathIsFreeFor( 'E1' ):
				self.setCrossingLanesToRed( 'E1' )
			else:
				if self.controller.floorPlan['F1']['hasTraffic']:
					self.setLight( 'F1', self.green)
				elif self.controller.floorPlan['F2']['hasTraffic']:
					self.setLight( 'F2', self.green)
				self.setLight( 'E1', self.green)

		random.shuffle( self.lightEvaluationOrder )

		for light in self.lightEvaluationOrder:
			info = self.controller.floorPlan[light]

			if info['colour'] == self.red:
				if info['hasTraffic']:
					if self.pathIsFreeFor( light ):
						self.setLight(light, self.green)
					# Oh noes! People have been waiting for 2.5 minutes and they've still not gotten green!
					# They might be in a hurry, better give them some green.
					elif info['ticks'] > 60:
						self.setCrossingLanesToRed( light )
				# We've seen enough red, lets see some green instead!
				# This is mainly here to assist simulators that have trouble letting know if traffic is waiting.
				# After about 60 seconds, a light will go green when it it safe to do so.
				# Also, it confuses the drivers, so that's always a plus.
				elif self.pathIsFreeFor( light ) and info['ticks'] > self.randomJumpGreenTime( light ) and light != 'D1':
					self.setLight(light, self.green)

	def setCrossingLanesToRed( self, light : str ):
		for laneLight in self.FreeMap[light]:
			if self.controller.floorPlan[laneLight]['colour'] == self.green:
				self.setLight(laneLight, self.orange)

	def setLight( self, light : str, colour : str ):
		"""
		Set a specific light to a specific colour.
		This also reset the timer for that light back to 0.

		:param light: traffic light code
		:type light: str
		:param colour: traffic light colour
		:type colour: str
		"""
		self.controller.floorPlan[light]['colour'] = colour
		self.controller.floorPlan[light]['ticks'] = 0

	def pathIsFreeFor( self, light : str ) -> bool:
		"""
		Determines if the paths crossing light are free (set to red).

		:param light: traffic light code
		:type light: str
		:return: If the paths crossing light are free
		:rtype bool
		"""
		for blocker in self.FreeMap[light]:
			if self.controller.floorPlan[blocker]['colour'] != self.red:
				return False

		return True

	def getOrangeLightDuration( self, light: str ) -> int:
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
			'E': 2   # 2 seconds
		}

		return durations[group]

	def getGreenLightDuration( self, light : str ) -> int:
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

	def randomJumpGreenTime( self, light : str ) -> int:
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
			'E': -1   # Not supported
		}

		return durations[group]

	def __str__( self ) -> str:
		return 'Heuristic'
