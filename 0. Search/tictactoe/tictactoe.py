"""
Tic Tac Toe Player
"""

import math
import random
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
    emptyCount, xCount, oCount = scanBoard(board)

    if(emptyCount == 9 or oCount == xCount):
        return X
    else:
        return O

def scanBoard(board):
    emptyCount = xCount = oCount = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j] == X):
                xCount += 1
            elif(board[i][j] == O):
                oCount += 1
            else:
                emptyCount += 1
        
    return emptyCount, xCount, oCount

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = []
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                possibleActions.append([i,j])

    return possibleActions
                



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board[action[0]][action[1]] = player(board)

    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    emptyCount, xCount, oCount = scanBoard(board)

    if(xCount >= 3 or oCount >= 3):
        for i in range(3):
            if(board[i][0] == board[i][1] == board[i][2]):
                if(board[i][0] == X):
                    return X
                elif(board[i][0] == O):
                    return O
            
            if(board[0][i] == board[1][i] == board[2][i]):
                if(board[0][i] == X):
                    return X
                elif(board[0][i] == O):
                    return O 

        if(board[0][0] == board[1][1] == board[2][2]):
                if(board[1][1] == X):
                    return X
                elif(board[1][1] == O):
                    return O 

        if(board[0][2] == board[1][1] == board[2][0]):
                if(board[1][1] == X):
                    return X
                elif(board[1][1] == O):
                    return O 



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    emptyCount, xCount, oCount = scanBoard(board)

    if(emptyCount == 0):
        return True
    elif(winner(board) in (X, O)):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(winner(board) == X):
        return 1
    elif(winner(board) == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board) == True):
        return None
    else:
        AI = player(board)
        actionValues = []
        possibleActions = actions(board)
        turns = 1

        emptyCount, xCount, oCount = scanBoard(board)

        if(emptyCount == 9 or emptyCount == 8):
            return random.choice(possibleActions)

        for action in possibleActions:
            oVal = xVal = 0
            testBoard = result(copy.deepcopy(board), action)
            if(terminal(testBoard) == True):
                return action
            oVal, xVal = rating(testBoard, turns, oVal, xVal)
            val = oVal + xVal
            actionValues.append(val) 
        
        if(AI == X):
            maxValIndex = actionValues.index(max(actionValues))
            return possibleActions[maxValIndex]
        if(AI == O):
            minValIndex = actionValues.index(min(actionValues))
            return possibleActions[minValIndex]
            
           
    raise NotImplementedError

def rating(board, turns, oVal, xVal):
    turns += 1
    for action in actions(board):
        testBoard = result(copy.deepcopy(board), action)
        if(terminal(testBoard) == True):
            w = winner(testBoard)
            if(w == X):
                temp = 1 - (turns/10)
                if(temp > xVal):
                    xVal = copy.deepcopy(temp)
            else:
                temp = -(1 - (turns/10))
                if(temp < oVal):
                    oVal = copy.deepcopy(temp)
        temp_oVal, temp_xVal = rating(testBoard, turns, oVal, xVal) 
        if(temp_oVal < oVal):
            oVal = copy.deepcopy(temp_oVal)
        if(temp_xVal > xVal):
            xVal = copy.deepcopy(temp_xVal)

    return oVal, xVal        