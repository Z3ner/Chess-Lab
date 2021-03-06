from player import *
import chess
import numpy as np
import collections
import math

def start_game(player1, player2, period_board = 1, add_pgn = None, verbose = True):

	if type(player1)==str:
		player1 = HumanPlayer(player1)
	if type(player2)==str:
		player2 = HumanPlayer(player2)

	print("Game:", player1.name,"vs",player2.name)

	"""
	if verbose:
		print("Game:", player1.name,"vs",player2.name)
	"""

	turn = 0
	state = chess.Board()

	while winner(state) == 0:

		if verbose and turn % period_board == 0:
			print(state)

		if turn % 2 == 0:

			move = player1.move(state)
			state.push_san(move)

			if verbose:
				print("Move:",move)

		else:

			move = player2.move(state)
			state.push_san(move)

			if verbose:
				print("Move:",move)

		turn += 1

	if verbose:
		print("###############################################################")
		print("Game:", player1.name,"vs",player2.name)
		print("Result:", state.result())
		print("Board:")
		print(state)
		print("Move:",move)
		print("###############################################################")

	return winner(state)

def tournament(list_players, loops = 2):

	n_players = len(list_players)
	scores = {}
	swap_players = False
	change = False

	for player in list_players:
		if type(player) == str:
			scores[player] = 0
		else:
			scores[player.name] = 0

	for _ in range(loops):

		i = 1

		for i in range(1, n_players):

			list_idx = [x for x in range(i, n_players)]

			for j in range(i, n_players):

				np.random.shuffle(list_idx)

				idx1 = i - 1
				idx2 = list_idx[0]

				list_idx = list_idx[1:]

				if (idx2 % 2 == 0 and swap_players == False) or (idx2 % 2 == 1 and swap_players == True):
					swap_players = swap_players ^ True

				if swap_players ^ change:
					playerW = list_players[idx2]
					playerB = list_players[idx1]
				else:
					playerW = list_players[idx1]
					playerB = list_players[idx2]

				if type(playerW)==str:
					playerW = HumanPlayer(playerW)
				if type(playerB)==str:
					playerB = HumanPlayer(playerB)

				result = start_game(playerW, playerB, verbose = False)

				scores[playerB.name] += result - 1
				scores[playerW.name] += 2 - result

		if n_players % 4 == 0 or n_players % 4 == 1:
			change = change ^ True

	print(scores)

	P = collections.namedtuple('P', 'score name')
	ranking = sorted([P(v,k) for (k,v) in scores.items()], reverse=True)

	print("Winner:", ranking[0].name, "Score:", ranking[0].score)

def swiss_system(list_players, shortcut = False):

	n_players = len(list_players)
	rounds = math.floor(math.log(n_players,2))

	actual_ranking = [(0, player) for player in list_players]

	for r in range(rounds):

		print("Round ", r + 1, "-", "Participans:", len(actual_ranking))
		np.random.shuffle(actual_ranking)
		actual_ranking = sorted(actual_ranking, key=takeFirst, reverse=True)

		if shortcut:
			score_max, _ = actual_ranking[0]
			for score, player in actual_ranking:
				if r < (rounds - 2):
					if (score_max + (rounds - r)/2) > (score + rounds - r):
						del actual_ranking[(score, player)]
				else:
					if score_max > (score + rounds - r):
						del actual_ranking[(score, player)]
					

		for idx in range(0, n_players, 2):

			scoreW, playerW = actual_ranking[idx]
			scoreB, playerB = actual_ranking[idx + 1]

			if type(playerW)==str:
				playerW = HumanPlayer(playerW)
			if type(playerB)==str:
				playerB = HumanPlayer(playerB)

			result = start_game(playerW, playerB, verbose = False)

			scoreB += result - 1
			scoreW += 2 - result

			actual_ranking[idx] = (scoreW, playerW)
			actual_ranking[idx+1] = (scoreB, playerB)

	actual_ranking = sorted(actual_ranking, key=takeFirst, reverse=True)
	final_score, winner = actual_ranking[0]
	print("Winner:", winner.name, "Score:", final_score)

	return winner


def takeFirst(elem):
	return elem[0]



def legal_plays(state):
		return [str(state.san(move)) for move in state.legal_moves]

def winner(state):

    if state.result()=='*':
        return 0
    elif state.result()=='1-0':
        return 1
    elif state.result()=='0-1':
        return 2
    elif state.result()=='1/2-1/2':
        return 1.5