"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    EmptySpaces = sum([line.count(EMPTY) for line in board])
    if EmptySpaces%2 == 0:
        # O's turn, if the number of EMPTY is Even
        return O
    # else (odd), it's X's turn
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    for i, row in enumerate(board):
        if row[0] == EMPTY:
            possibleActions.add((i,0))
        if row[1] == EMPTY:
            possibleActions.add((i,1))
        if row[2] == EMPTY:
            possibleActions.add((i,2))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception('action ({},{}) is not a valid option.'.format(i, j))
    newBoardState = copy.deepcopy(board)
    newBoardState[i][j] = player(board)
    return newBoardState


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i, row in enumerate(board):
        
        if row.count(row[0]) == len(row) and row[0] != EMPTY:
            # Rows
            # |X|X|X|      | | | |      | | | |
            # | | | |  OR  |O|O|O|  OR  | | | |
            # | | | |      | | | |      |X|X|X|
            return row[0]

        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            # Columns
            # |O| | |      | |X| |      | | |O|
            # |O| | |  OR  | |X| |  OR  | | |O|  
            # |O| | |      | |X| |      | | |O|
            return board[0][i]
    
    if (board[0][0] == board[1][1] == board[2][2] and board[1][1] != EMPTY) or (
        board[2][0] == board[1][1] == board[0][2] and board[1][1] != EMPTY):
        # Diagonals
        # |X| | |      | | |O|
        # | |X| |  OR  | |O| | 
        # | | |X|      |O| | |
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        # If have a winner, the game is over
        return True
    
    if sum([row.count(EMPTY) for row in board]) == 0:
        # And if doesn't have EMPTY spaces in the board, tie (the game is also over)
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    p = winner(board)
    if p == X:
        return 1
    if p == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    bestAction = None
    v = []
    if player(board) == X:
        # for action in actions(board):
        #     score = minValue(result(board, action))
        #     v.append((action, score))

        # v is a List of TUPLES, that have: 
        # action, and the best value the MIN player can obtain with this action, 
        # for all available actions in the board

        # Can write all this with a line:
        v = [(action, minValue(result(board, action))) for action in actions(board)]
        # bestAction is the action with the highest value in v list
        bestAction = max(v, key=lambda x: x[1])[0]
    else:
        # for action in actions(board):
        #     score = maxValue(result(board, action))
        #     v.append((action, score))

        # The same as X, but now, for O, the best value MAX player can obtain
        v = [(action, maxValue(result(board, action))) for action in actions(board)]
        # And now, bestAction is the action with the smallest value in v list
        bestAction = min(v, key=lambda x: x[1])[0]
    return bestAction

def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v
