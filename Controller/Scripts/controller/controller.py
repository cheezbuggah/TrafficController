from typing import Iterator
from logging import Logger
from abc import ABC, abstractmethod
import sys
import json


class Algorithm(ABC):
	logger: Logger

	def __init__(self):
		self.controller = None
		self.Logger = None

	def set_controller(self, controller):
		self.controller = controller

	def set_logger(self, logger: Logger):
		self.logger = logger

	@abstractmethod
	def calculate_new_floor_plan(self):
		pass

	@abstractmethod
	def __str__(self):
		pass


class No(Algorithm):
	def calculate_new_floor_plan(self):
		pass

	def __str__(self):
		return 'No'


class Controller:
	#traffic lights

	red_light = 'red'
	orange_light = 'orange'
	yellow_light = orange_light
	green_light = 'green'

	lights_car = [
		'A1',
		'A2',
		'A3',
		'A4',
		'A5',
		'A6',
		'A7',
		'A8',
		'A9',
		'A10'
	]

	lights_cyclist = [
		'B1',
		'B2',
		'B3'
	]

	lights_pedestrian = [
		'C1.1',
		'C1.2',
		'C2.1',
		'C2.2',
		'C3.1',
		'C3.2'
	]

	lights_bus = [
		'D1'
	]

	lights_train = [
		'E1',
		'F1',
		'F2'
	]

	lights_all = lights_car + lights_cyclist + lights_pedestrian + lights_bus + lights_train

	def __init__(self, logger: Logger):
		self.floorPlan = {}
		self.logger = logger
		self.algorithm = None

	def set_algorithm(self, algorithm: Algorithm):
		algorithm.set_logger(self.logger)
		algorithm.set_controller(self)
		self.algorithm = algorithm
		self.logger.info('Set to use algorithm ' + str(algorithm))

	def prepare_floor_plan(self):
		for light in Controller.lights_all:
			self.floorPlan[light] = {
				'colour': Controller.red_light,
				'timer': None,
				'hasTraffic': False,
				'ticks': 0
			}

	def get_floor_plan(self) -> Iterator[dict]:
		for light, data in self.floorPlan.items():
			light_info = {
				'light': light,
				'status': data['colour'],
				'timer': data['timer']
			}

			if data['timer'] is not None:
				light_info['timer'] = data['timer']

			yield light_info

	def calculate_floor_plan(self):
		self.algorithm.calculate_new_floor_plan()

	def queue_traffic(self, target: str):
		if target == 'F1' or target == 'F2':
			self.queue_traffic('E1')

		if target not in Controller.lights_all:
			# raise ValueError( 'Not a supported traffic light' )
			self.logger.warning('Unsupported traffic light ' + target)

		self.floorPlan[target]['hasTraffic'] = True
