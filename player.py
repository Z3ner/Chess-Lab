from abc import ABCMeta,abstractmethod

import numpy as np
import chess
import chess.engine
from game import *

class Player:
  
	__metaclass__ = ABCMeta

	@abstractmethod
	def move(self, state):
		pass

class HumanPlayer(Player):

	def __init__(self, name):

		self.name = name

	def move(self, state):

		move = ""
		while move not in [m for m in self.legal_plays(state)]:
			move = input("Mueve: ")

		return move

	def legal_plays(self, state):
		return [str(state.san(move)) for move in state.legal_moves]

class RandomPlayer(Player):

	def __init__(self):

		self.name = "RandomPlayer"

	def move(self, state):

		possible_moves = legal_plays(state)
		np.random.shuffle(possible_moves)

		return possible_moves[0]

class Stockfish(Player):

	def __init__(self, max_time = 2):

		self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_10_x64")
		self.name = self.engine.id.get("name")
		self.max_time = max_time

	def move(self, state):

		result = self.engine.play(state, chess.engine.Limit(time=self.max_time))

		return state.san(result.move)
	

