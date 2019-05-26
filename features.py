from game import *



def is_checkmate_next(state, color):

	for move in legal_plays(state):
		if move[-1] == '#':
			if color:
				return 1
			else:
				return -1

	return 0


def get_number_pawns(state, color):
	count = 0
	for square in str(state):
		if color:
			if square == 'P':
				count += 1
			else:
				pass
		else:
			if square == 'p':
				count += 1
			else:
				pass
	return count

def get_number_knights(state, color):
	count = 0
	for square in str(state):
		if color:
			if square == 'N':
				count += 1
			else:
				pass
		else:
			if square == 'n':
				count += 1
			else:
				pass
	return count

def get_number_bishops(state, color):
	count = 0
	for square in str(state):
		if color:
			if square == 'B':
				count += 1
			else:
				pass
		else:
			if square == 'b':
				count += 1
			else:
				pass
	return count

def get_number_rocks(state, color):
	count = 0
	for square in str(state):
		if color:
			if square == 'R':
				count += 1
			else:
				pass
		else:
			if square == 'r':
				count += 1
			else:
				pass
	return count

def get_number_queens(state, color):
	count = 0
	for square in str(state):
		if color:
			if square == 'Q':
				count += 1
			else:
				pass
		else:
			if square == 'q':
				count += 1
			else:
				pass
	return count