from abc import ABCMeta,abstractmethod
from player import *
import numpy as np
from encode import *
from game import *

class OneEvalPlayer(Player):

	__metaclass__ = ABCMeta

	def __init__(self, name):

		self.name = name

	def move(self, state):

		action_values = []

		for m in self.legal_plays(state):
			state.push_san(m)
			action_values += [(self.eval(state), m)]
			state.pop()

		if state.turn:
			_, move = max(action_values)
		else:
			_, move = min(action_values)

		return move

	@abstractmethod
	def eval(self, state):
		pass


class GeneticMatrix(OneEvalPlayer):

	def __init__(self, name = "GeneticMatrix", centers = [0]*18, radio = 2.5):

		OneEvalPlayer.__init__(self, name)
		self.generate_kernels(centers = centers, radio = radio)

	def eval(self, state):
		result = 0
		m = encode_state(state)
		for i in range(6):
			for j in range(6):
				for k in range(12):
					result += np.sum(np.multiply(m[i:i+3, j:j+3, k],self.kernels[k]))

		return result

	def generate_kernels(self, centers = [0]*18, radio = 2.5):

		self.kernels = []
		sign = 1
		for i in range(12):
			if i == 6:
				sign = -1

			w1 = sign*np.random.uniform(centers[(i%6)*3] - radio, centers[(i%6)*3] + radio)
			w2 = sign*np.random.uniform(centers[(i%6)*3 + 1] - radio, centers[(i%6)*3 + 1] + radio)
			w3 = sign*np.random.uniform(centers[(i%6)*3 + 2] - radio, centers[(i%6)*3 + 2] + radio)

			self.kernels += [np.array([[w3, w2, w3],[w2, w1, w2],[w3, w2, w3]])]

	def insert_coefs(self, coefs):

		if len(coefs) != 18:
			return

		self.kernels = []

		sign = 1
		for i in range(12):
			if i == 6:
				sign = -1

			w1 = sign*np.random.uniform(coefs[(i%6)*3], coefs[(i%6)*3])
			w2 = sign*np.random.uniform(coefs[(i%6)*3 + 1], coefs[(i%6)*3 + 1])
			w3 = sign*np.random.uniform(coefs[(i%6)*3 + 2], coefs[(i%6)*3 + 2])

			self.kernels += [np.array([[w3, w2, w3],[w2, w1, w2],[w3, w2, w3]])]

	def get_coefs(self):

		coefs = []

		for kernel in self.kernels[:6]:

			coefs += [kernel[1][1]]
			coefs += [kernel[0][1]]
			coefs += [kernel[0][0]]

		return coefs


def genetic_algorithm(centers = [1]*18, radio = 1, n = 100, reduction = 0.1, last_winner = None):

	if radio == 0:
		return last_winner

	if last_winner == None:
		last_winner = GeneticMatrix("Genetic"+str(n-1), centers = centers, radio = radio)

	swiss_players = [GeneticMatrix("Genetic"+str(i), centers = centers, radio = radio) for i in range(n-1)]
	swiss_players += [last_winner]
	winner = swiss_system(swiss_players, shortcut = True)
	print(winner.get_coefs())
	winner.name = "WinnerGM"

	return genetic_algorithm(centers=winner.get_coefs(), radio= radio - reduction, n=n, last_winner = winner)


