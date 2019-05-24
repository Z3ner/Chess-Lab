import chess

def start_game(player1, player2, period_board = 1, add_pgn = None, verbose = True):

	if verbose:
		print("Game:", player1.name,"vs",player2.name)

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

	if verbose:
		print("###############################################################")
		print("Game:", player1.name,"vs",player2.name)
		print("Result:", state.result())
		print("Board:")
		print(state)
		print("Move:",move)
		print("###############################################################")

	return winner(state)


def winner(state):

    if state.result()=='*':
        return 0
    elif state.result()=='1-0':
        return 1
    elif state.result()=='0-1':
        return 2
    elif state.result()=='1/2-1/2':
        return -1