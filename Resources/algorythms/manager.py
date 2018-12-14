from typing import List
from Resources.algorythms.randomizer import Randomizer
#from Resources.algorythms.heuristic import Heuristic
from Resources.algorythms.disco import Disco
from Resources.algorythms.zondagsrust import ZondagsRust
from Resources.algorythms.heuristic_KS import Heuristic
from Resources.algorythms.test import Test


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
