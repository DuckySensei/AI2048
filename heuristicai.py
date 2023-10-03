import random
import game
import sys

# Author:				chrn (original by nneonneo) automated logic by Dylan Toomey
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

#int for move count
moveCount = -1

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    bestmove = -1    
	
	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    # bestmove = find_best_move_random_agent()
    bestmove = make_best_move(board)
    return bestmove

def make_best_move(board):

    #increment movecount by 1
    global moveCount
    moveCount += 1
    
    #move all the pieces to the left
    if moveCount == 0:
        return LEFT
    if moveCount == 1:
        return DOWN
    
    #check to see if the bottom of the board is full of all different numbers
    bottom_full = check_bottom_row(board)

    #check it first row is stacked all the way up
    top_full = check_top_row(board)

    
    whichMove = check_adjacent_tiles(board)
    if whichMove != False:
        if bottom_full == False and top_full == False:
            
            #choose whichmove IF which move is left or down
            if whichMove == LEFT or whichMove == DOWN:
                return whichMove
            else:
                return random.choice([DOWN, LEFT])
            
        if bottom_full == False and top_full == True:
            

            #choose whichmove If which move is left up or down
            if whichMove == LEFT or whichMove == DOWN or whichMove == UP:
                return whichMove
            else:
                return random.choice([DOWN, LEFT, UP])
            
        if bottom_full == True and top_full == False:

            #choose whichmove If which move is left or down or right
            if whichMove == LEFT or whichMove == DOWN or whichMove == RIGHT:
                return whichMove
            else:
                return random.choice([DOWN, LEFT, RIGHT])
            
        #if none of the above are hit, just choose which move
        return whichMove
    else:
        if bottom_full == False and top_full == False:
            return random.choice([DOWN, LEFT])
        if bottom_full == False and top_full == True:
            return random.choice([DOWN, LEFT, UP])
        if bottom_full == True and top_full == False:
            return random.choice([DOWN, LEFT, RIGHT])
        #if none of the above are hit, just choose which move
        return random.choice([DOWN, LEFT, RIGHT, UP])


    # if no adjacent tiles have the same value, move randomly
    return random.choice([UP, DOWN, LEFT, RIGHT])

def check_bottom_row(board):
    for i in range(4):
        if board[i][3] == 0 or board[i][3] == board[3][3]:
            return False
        else:
            if board[i][3] == board[i+1][3]:
                return False
    return True

def check_top_row(board):
    for i in range(4):
        if board[3][i] == 0 or board[3][i] == board[3][3]:
            return False
        else:
            if board[3][i] == board[3][i+1]:
                return False
    return True
    
    
def check_adjacent_tiles(board):
    leftFavorable = 0
    rightFavorable = 0
    topFavorable = 0
    bottomFavorable = 0

    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                # check left tile
                if j > 0 and board[i][j-1] == board[i][j]:
                    leftFavorable += 1
                # check right tile
                if j < 3 and board[i][j+1] == board[i][j]:
                    rightFavorable += 1
                # check top tile
                if i > 0 and board[i-1][j] == board[i][j]:
                    topFavorable += 1
                # check bottom tile
                if i < 3 and board[i+1][j] == board[i][j]:
                    bottomFavorable += 1

    #get which number is highest of left right top and bottom
    highest = max(leftFavorable, rightFavorable, topFavorable, bottomFavorable)

    if highest == 0:
        return False

    #if the highest is left
    if highest == leftFavorable:
        return LEFT
    #if the highest is right
    if highest == rightFavorable:
        return RIGHT
    #if the highest is top
    if highest == topFavorable:
        return UP
    #if the highest is bottom
    if highest == bottomFavorable:
        return DOWN



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
