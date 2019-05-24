from abc import ABCMeta,abstractmethod

import numpy as np

class Player:
  
	__metaclass__ = ABCMeta

	def legal_plays(self, state):
		return [str(state.san(move)) for move in state.legal_moves]

	@abstractmethod
	def move(self, state):
		pass

class RandomPlayer(Player):

	def __init__(self):

		self.name = "RandomPlayer"

	def move(self, state):

		possible_moves = self.legal_plays(state)
		np.random.shuffle(possible_moves)

		return possible_moves[0]

	

