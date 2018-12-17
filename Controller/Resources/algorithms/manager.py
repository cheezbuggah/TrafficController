from typing import List
from Resources.algorithms.randomizer import Randomizer
#from Resources.algorithms.heuristic import Heuristic
from Resources.algorithms.disco import Disco
from Resources.algorithms.zondagsrust import ZondagsRust
from Resources.algorithms.heuristic_algorithm import Heuristic
from Resources.algorithms.test import Test


class Manager:
	def __init__(self):
		algorithms = [
			Randomizer(),
			Heuristic(),
			Disco(),
			ZondagsRust(),
			Test()
		]

		self.algorithms = {}

		for algorithm in algorithms:
			name: str = str(algorithm)
			self.algorithms[name] = algorithm

	def get_algorithm_names(self) -> List[str]:
		return list(self.algorithms.keys())

	def get_algorithm(self, name: str):
		if name not in self.get_algorithm_names():
			raise NameError("Not a known algorithm: " + name)

		return self.algorithms[name]
