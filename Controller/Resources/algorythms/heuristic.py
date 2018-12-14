import random
from typing import Dict
from typing import List
from Scripts.controller.controller import Algorithm
from Scripts.controller.controller import Controller


class Heuristic(Algorithm):
	# Dictionary van alle verkeerslichten om te bepalen welke lichten rood moeten zijn
	# om het eerste licht op groen te zetten.
	# Voorbeeld: als A1 groen moet zijn, moeten A5,A7,B1,C1.1,C3.2 en D1 op rood staan.

	LightMapAll: Dict[str, List[str]] = {
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
		self.evaluation_order: List[str] = list(self.LightMapAll.keys())[:-3]

	# Methode om te kijken of een pad vrij is
	def check_path_free(self, path: str) -> bool:
		for lane in self.LightMapAll[path]:
			if self.controller.floorPlan[lane]['colour'] != self.red:
				return False

			return True

	# Methode om op een snelle manier een licht op een bepaalde kleur te zetten
	def set_light(self, light: str, colour: str):
		self.controller.floorPlan[light]['colour'] = colour
		self.controller.floorPlan[light]['ticks'] = 0

	# Methode om de kruisende banen van een stoplicht op rood te zetten, zodat het betreffende
	# stoplicht op groen kan.
	def cross_stop(self, path: str):
		for lane in self.LightMapAll[path]:
			if self.controller.floorPlan[lane]['colour'] == self.green:
				self.set_light(path, self.orange)

	#tijdsduur dat een stoplicht op groen mag staan
	def green_duration(self, light: str) -> int:
		group = light[0]
		if group == 'F':
			group = 'E'

		durations = {
			'A': 7,  # 7 seconden
			'B': 7,  # 7 seconden
			'C': 5,  # 5 seconden
			'D': 4,  # 4 seconden
			'E': 30  # 30 seconden
		}

		return durations[group]

	#tijdsduur dat een stoplicht op oranje mag staan
	def orange_duration(self, light: str) -> int:
		group = light[0]
		if group == 'F':
			group = 'E'

		durations = {
			'A': 4,  # 4 seconden
			'B': 2,  # 2 seconden
			'C': 2,  # 2 seconden
			'D': 4,  # 4 seconden
			'E': 2   # 2 seconden
		}

		return durations[group]

	#verkeerslichten na een bepaalde tijd op groen zetten als een grote tijdsduur is verstreken zonder verkeer
	def random_green_time(self, light: str) -> int:
		group = light[0]
		if group == 'F':
			group = 'E'

		durations = {
			'A': 60,  # 60 seconden
			'B': 100,  # 100 seconden
			'C': 100,  # 120 seconden
			'D': -1,  # Niet ondersteund door controller
			'E': -1   # Niet ondersteund door controller
		}

		return durations[group]

	# De plattegrond samenstellen op basis van waar verkeer staat en hoe lang dit verkeer er al staat
	def calculate_new_floor_plan(self):

		for light, info in self.controller.floorPlan.items():
			info['ticks'] += 1

			orange_duration = self.orange_duration(light)
			green_duration = self.green_duration(light)

			if info['colour'] == self.green and info['ticks'] > green_duration:
					self.set_light(light, self.orange)
					info['hasTraffic'] = False
					if light == 'E1':
						self.set_light('F1', self.orange)
						self.controller.floorPlan['F1']['hasTraffic'] = False
						self.set_light('F2', self.orange)
						self.controller.floorPlan['F2']['hasTraffic'] = False

			elif info['colour'] == self.orange and info['ticks'] > orange_duration:
				self.set_light(light, self.red)
				if light == 'E1':
					self.set_light('F1', self.red)
					self.set_light('F2', self.red)

		# busstoplicht: altijd hoogste prioriteit van gemotoriseerd verkeer
		if self.controller.floorPlan['D1']['hasTraffic'] and self.controller.floorPlan['D1']['colour'] == self.red:
			if not self.check_path_free('D1'):
				if self.controller.floorPlan['D1']['ticks'] > 10:
					self.cross_stop('D1')
			else:
				self.set_light('D1', self.green)

		#treinstoplicht; altijd hoogste prioriteit, trein stopt niet
		if self.controller.floorPlan['E1']['hasTraffic'] is True and self.controller.floorPlan['E1']['colour'] == self.red:
			if self.check_path_free('E1') is False:
				self.cross_stop('E1')
			else:
				if self.controller.floorPlan['F1']['hasTraffic'] is True:
					if self.controller.floorPlan['F2']['hasTraffic'] is False:
						self.set_light('F1', self.green)
					self.set_light('F2', self.green)
				self.set_light('E1', self.green)

		#Stoplichten op rood zetten in een aparte loop om herhalende voorrang te voorkomen
		random.shuffle(self.evaluation_order)

		for light in self.evaluation_order:
			info = self.controller.floorPlan[light]
			green_time = self.green_duration(light)

			if info['colour'] is self.red:
				if info['hasTraffic'] is True:
					if self.check_path_free(light):
						self.set_light(light, self.green)
					elif info['ticks'] > 120:
						self.cross_stop(light)
				elif self.check_path_free(light) and info['ticks'] > green_time and light != 'D1':
					self.set_light(light, self.green)

	def __str__(self):
		return 'Heuristic'


