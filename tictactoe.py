"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np
import random
import time

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
    x_count = 0
    o_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1
    if x_count > o_count:
        return O
    elif x_count <= o_count:
        return X
    else:
        return X 
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    selection = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                selection.append((i,j))
    return selection

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def row_win(board, player):
    b = np.array(board)
    check_board = b == player
    for row in check_board:
        if np.all(row):
            return True
    return False

def col_win(board, player):
    b = np.array(board)
    check_board = b == player 
    for col in range(3):
        if np.all(check_board[:,col]):
            return True
    return False 

def diag_win(board, player):
    b = np.array(board)
    if np.all(np.diagonal(b) == player):
        return True
    if np.all(np.diagonal(np.fliplr(b)) == player):
        return True 
    return False 


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if row_win(board, X) or col_win(board, X) or diag_win(board, X):
        return X

    elif row_win(board, O) or col_win(board, O) or diag_win(board, O):
        return O
    else:
        return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    #check if there is an empty slot in the board
    for row in board:
        if EMPTY in row:
            return False
    #board is filled
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    util = winner(board)
    if util == X:
        return 1
    if util == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == initial_state():
        x = random.choice([0,1,2])
        y = random.choice([0,1,2])
        return (x,y)
    if terminal(board):
        return None
    p = player(board)
    m = 0
    mov = actions(board)[0]
    start = time.clock()
    if p == X:
        for action in actions(board):
            v = max_value(result(board,action), 0)
            if v >= m:
                m = v
                mov = action 
        end = time.clock()
        print("AI Move time: ",end - start)
        return mov
        
    else:
        for action in actions(board):
            v = min_value(result(board,action), 0)
            if v <= m:
                m = v
                mov = action 
        end = time.clock()
        print("AI Move time: ",end - start)
        return mov



def max_value(board,level):
    if terminal(board):
        return utility(board)
    if level == 999:
        return 0
    v = - math.inf
    for action in actions(board):
        v = max(v, min_value(result(board,action),level + 1)) 
    return v 

def min_value(board, level):
    if terminal(board):
        return utility(board)
    if level == 999:
        return 0
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board,action), level + 1)) 
    return v 

