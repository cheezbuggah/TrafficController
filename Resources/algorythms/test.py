from Scripts.controller.controller import Controller
from Scripts.controller.controller import Algorithm


class Test(Algorithm):
	def __init__(self):
		super().__init__()
		self.counter = 0
		self.light_index, carIndex, cyclistIndex, pedestrianIndex, busIndex, trainIndex = 0, 0, 0, 0, 0, 0
		self.carLights, cyclistLights, pedestrianLights, busLights, trainLights = Controller.lights_car, Controller.lights_cyclist, Controller.lights_pedestrian, Controller.lights_bus, Controller.lights_train
		self.red, green, orange = Controller.red_light, Controller.green_light, Controller.orange_light
		self.colour = Controller.red_light
		self.light = 'A1'

	def yield_light(self):
		self.light_index += 1

		if self.light_index == len(Controller.lights_all):
			self.light_index = 0

		return Controller.lights_all[self.light_index]

	def calculate_new_floor_plan(self):
		# Count to 10 as to end up with 1 second.
		if self.counter < 15:
			self.counter += 1
			return
		else:
			self.counter = 0

		update_light = False

		if self.colour == Controller.red_light:
			self.colour = Controller.green_light
		elif self.colour == Controller.orange_light:
			self.colour = Controller.red_light
			update_light = True
		elif self.colour == Controller.green_light:
			self.colour = Controller.orange_light

		print('Setting ' + self.light + ' to ' + self.colour)

		self.controller.floorPlan[self.light]['colour'] = self.colour

		if update_light:
			self.light = self.yield_light()

	def __str__(self):
		return 'Test'
