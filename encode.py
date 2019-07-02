import numpy as np

def encode_state(state):

	planes = []

	planes += [encode_pawns(state)]
	planes += [encode_knights(state)]
	planes += [encode_bishops(state)]
	planes += [encode_rooks(state)]
	planes += [encode_queens(state)]
	planes += [encode_kings(state)]
	planes += [encode_pawns(state, color = False)]
	planes += [encode_knights(state, color = False)]
	planes += [encode_bishops(state, color = False)]
	planes += [encode_rooks(state, color = False)]
	planes += [encode_queens(state, color = False)]
	planes += [encode_kings(state, color = False)]

	planes = np.asarray(planes)

	return np.reshape(planes, [8, 8, 12])

def encode_pawns(state, color=True):
	position = []
	for square in str(state):
		if color:
			if square == 'P':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]
		else:
			if square == 'p':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]

	return position

def encode_knights(state, color=True):
	position = []
	for square in str(state):
		if color:
			if square == 'N':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]
		else:
			if square == 'n':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]

	return position

def encode_bishops(state, color=True):
	position = []
	for square in str(state):
		if color:
			if square == 'B':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]
		else:
			if square == 'b':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]

	return position

def encode_rooks(state, color=True):
	position = []
	for square in str(state):
		if color:
			if square == 'R':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]
		else:
			if square == 'r':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]

	return position

def encode_queens(state, color=True):
	position = []
	for square in str(state):
		if color:
			if square == 'Q':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]
		else:
			if square == 'q':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]

	return position

def encode_kings(state, color=True):
	position = []
	for square in str(state):
		if color:
			if square == 'K':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]
		else:
			if square == 'k':
				position += [1]
			elif square == ' ' or square =='\n':
				pass
			else:
				position += [0]

	return position
