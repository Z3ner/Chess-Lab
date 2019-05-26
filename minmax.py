from abc import ABCMeta,abstractmethod
import numpy as np
from game import *
from player import *
from features import *
from time import time

class Node:

	def __init__(self, value, white = True):

		self.value = value
		self.children = {}
		self.white = white

	def update(self):

		if len(self.children) == 0:
			return self.value

		if self.white:
			self.value = max(child.update() for action, child in self.children.items())
		else:
			self.value = min(child.update() for action, child in self.children.items())

		return self.value

	def get_best_move(self):

		if self.white:
			_, move = max((child.value, action) for action, child in self.children.items())
		else:
			_, move = min((child.value, action) for action, child in self.children.items())

		return move


"""

Only to measure performance comparisons

"""
class BruteForcePlayer(Player):

	__metaclass__ = ABCMeta

	def __init__(self, name, max_time = 2000, max_depth = 2):

		self.name = name
		self.max_time = max_time
		self.max_depth = max_depth
		self.root = None

	def move(self, state):

		if self.root == None:
			self.root = Node(self.eval(state), state.turn)
		else:
			move = state.pop()
			self.root = self.root.children[state.san(move)]	
			state.push_san(state.san(move))

		self.expand_tree(state)
		self.root.update()
		move = self.root.get_best_move()
		self.root = self.root.children[move]

		return move


	def expand_tree(self, state):

		self.start_time = time()
		top_depth = 1

		while top_depth <= self.max_depth and self.max_time >= (time() - self.start_time):
			self.expand_rec(self.root, state, 0, top_depth)
			top_depth += 1
			print(time() - self.start_time)

	def expand_rec(self, node, state, depth, top_depth):

		if depth > self.max_depth or top_depth <= depth or self.max_time < (time() - self.start_time):
			return

		if len(node.children):
			for action, child in node.children.items():
				state.push_san(action)
				self.expand_rec(child, state, depth+1, top_depth)
				state.pop()

		possible_moves = legal_plays(state)
		for move in possible_moves:
			state.push_san(move)
			node.children[move] = Node(self.eval(state), white = state.turn)
			self.expand_rec(node.children[move], state, depth+1, top_depth)
			state.pop()

		return

	@abstractmethod
	def eval(self, state):
		pass

class Dummy(BruteForcePlayer):

	def __init__(self, name = "Dummy"):

		BruteForcePlayer.__init__(self, name)

	def eval(self, state):
		return 0

class Material1BF(BruteForcePlayer):

	def __init__(self, name = "Material1BF"):

		BruteForcePlayer.__init__(self, name)

	def eval(self, state):
		return np.random.uniform(-0.2,0.2) + (get_number_pawns(state, True)*1 + get_number_knights(state, True)*3 + get_number_knights(state, True)*3 + get_number_rocks(state, True)*5 + get_number_queens(state, True)*9) - (get_number_pawns(state, False)*1 + get_number_knights(state, False)*3 + get_number_knights(state, False)*3 + get_number_rocks(state, False)*5 + get_number_queens(state, False)*9)

class CheckMateBF(BruteForcePlayer):

	def __init__(self, name = "CheckMateBF"):

		BruteForcePlayer.__init__(self, name)

	def eval(self, state):

		checkmate = 0

		if winner(state) == 1 and state.turn == False:
			checkmate = 10000
		elif winner(state) == 2 and state.turn == True:
			checkmate = -10000
		else:
			checkmate = is_checkmate_next(state, state.turn)*1000


		return checkmate + np.random.uniform(-0.2,0.2) + (get_number_pawns(state, True)*1 + get_number_knights(state, True)*3 + get_number_knights(state, True)*3 + get_number_rocks(state, True)*5 + get_number_queens(state, True)*9) - (get_number_pawns(state, False)*1 + get_number_knights(state, False)*3 + get_number_knights(state, False)*3 + get_number_rocks(state, False)*5 + get_number_queens(state, False)*9)