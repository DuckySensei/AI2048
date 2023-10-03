import random
import game
import sys

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
moveCount = 0
scoreSame = 0
repeater = 0

def find_best_move(board):
    bestmove = -1    
	
	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    #bestmove = find_best_move_random_agent()
    bestmove = getbestmove(board)
    return bestmove

def getbestmove(board):
    best_move = None

    #The first 2 moves are left and down
    global moveCount

    if moveCount == 0:
        moveCount += 1
        return LEFT
    elif moveCount == 1:
        moveCount += 1
        return DOWN
    
    #check for the strongest combination
    best_combo = catch_best_combo(board)
    #this ^^ works

    bottom_row = check_bottom_row(board)

    vertical_row = check_vertical_row(board)

    curScore = calculate_score(board)
    
    pickRand = repeat_move(curScore)

    best_move = catch_best_move(board, best_combo, bottom_row, vertical_row, pickRand)

    return best_move

def check_vertical_row(board):
    #get values you on the bottom row
    vertical_row = board[0]
    #check if there are any empty tiles
    for i in range(len(vertical_row)):
        if vertical_row[i] == 0:
            print("vertical row false")
            return False
    
    #check if 2 values are the same and next to each other [8,2,0,2] -> [8,4,0,0] so FALSE
    for i in range(len(vertical_row)):
        if i < len(vertical_row) - 1 and vertical_row[i] == vertical_row[i+1]:
            print("vertical row false")
            return False

    return True

def check_bottom_row(board):
    #get values you on the bottom row
    bottom_row = board[3]
    #check if there are any empty tiles
    for i in range(len(bottom_row)):
        if bottom_row[i] == 0:
            print("bottom row false")
            return False
    
    #check if 2 values are the same and next to each other [8,2,0,2] -> [8,4,0,0] so FALSE
    for i in range(len(bottom_row)):
        if i < len(bottom_row) - 1 and bottom_row[i] == bottom_row[i+1]:
            print("bottom row false")
            return False
  
    return True

def catch_best_move(board, best_combo, bottom, vert, pickRand):
    #if the score is the same for 10 moves, then we make a random move
    if (pickRand == True):
        if (vert == True):
            return random.choice([DOWN,LEFT,RIGHT])
        
        if (bottom == True):
            return random.choice([LEFT,UP,RIGHT])
        
        if bottom == True and vert == True:
            return random.choice([UP,RIGHT])
        
        return random.choice([DOWN,LEFT,RIGHT,UP])

    if (best_combo == LEFT or best_combo == DOWN):
        return best_combo
    
    if (best_combo == RIGHT):
        if (bottom == True):
            return RIGHT
        
    if (best_combo == UP):
        if (vert == True):
            return UP
    
    #now we make random moves depending on whether bottom and vertical are true
    if (bottom == True and vert == True):
        return random.choice([UP,RIGHT])
    if (bottom == True):
        return random.choice([LEFT,DOWN,RIGHT])
    
    if (vert == True):
        return random.choice([UP,LEFT,RIGHT])
    
    return random.choice([DOWN,LEFT])


def catch_best_combo(board):
    best_combo = 0
    best_combo_value = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                continue

            # Check for a matching tile to the right
            if j < len(board[i]) - 1 and board[i][j] == board[i][j+1]:
                combo_value = board[i][j] * 2
                if combo_value > best_combo_value:
                    best_combo = RIGHT
                    best_combo_value = combo_value

            # Check for a matching tile below
            if i < len(board) - 1 and board[i][j] == board[i+1][j]:
                combo_value = board[i][j] * 2
                if combo_value > best_combo_value:
                    best_combo = DOWN
                    best_combo_value = combo_value

    #print the value of the best combination
    return best_combo

def find_best_move_random_agent():
    return random.choice([UP,DOWN,LEFT,RIGHT])
    
def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")
		
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  

def calculate_score(board):
    """
    Given a board, calculates the current score based on the tile values.
    Returns an integer representing the score.
    """
    score = 0
    for row in board:
        for tile in row:
            score += tile
    return score

def repeat_move(curScore):
    global scoreSame
    global repeater
    print("scoreSame: " + str(repeater))
    if curScore >= scoreSame -3 and curScore <= scoreSame + 3:
        repeater += 1
    else:
        scoreSame = curScore
        repeater = 0

    if repeater == 10:
        repeater = 0
        return True
    
    return False
