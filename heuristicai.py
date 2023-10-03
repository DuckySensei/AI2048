import random
import game
import math
import sys

# Author:				chrn (original by nneonneo)
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
    moveCount = 0
    # move all the pieces to the left
    if moveCount == 0:
        moveCount += 1
        return LEFT
    # move all the pieces down
    if moveCount == 1:
        moveCount += 1
        return DOWN
    # use a heuristic function to evaluate the board state
    scores = [get_heuristic_score(move, board) for move in [UP, DOWN, LEFT, RIGHT]]
    # choose the move that maximizes the heuristic score
    return [UP, DOWN, LEFT, RIGHT][scores.index(max(scores))]

def sum_of_tile_values(board):
    return sum(sum(row) for row in board)

def smoothness(board):
    smoothness = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                value = math.log2(board[i][j])
                # check left tile
                if j > 0 and board[i][j-1] != 0:
                    smoothness -= abs(value - math.log2(board[i][j-1]))
                # check right tile
                if j < 3 and board[i][j+1] != 0:
                    smoothness -= abs(value - math.log2(board[i][j+1]))
                # check top tile
                if i > 0 and board[i-1][j] != 0:
                    smoothness -= abs(value - math.log2(board[i-1][j]))
                # check bottom tile
                if i < 3 and board[i+1][j] != 0:
                    smoothness -= abs(value - math.log2(board[i+1][j]))
    return smoothness

def monotonicity(board):
    monotonicity_left = 0
    monotonicity_right = 0
    monotonicity_up = 0
    monotonicity_down = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                # check left tiles
                if j > 0:
                    if board[i][j-1] == 0:
                        monotonicity_left += math.log2(board[i][j])
                    elif board[i][j-1] >= board[i][j]:
                        monotonicity_left += math.log2(board[i][j]) - math.log2(board[i][j-1])
                # check right tiles
                if j < 3:
                    if board[i][j+1] == 0:
                        monotonicity_right += math.log2(board[i][j])
                    elif board[i][j+1] >= board[i][j]:
                        monotonicity_right += math.log2(board[i][j]) - math.log2(board[i][j+1])
                # check top tiles
                if i > 0:
                    if board[i-1][j] == 0:
                        monotonicity_up += math.log2(board[i][j])
                    elif board[i-1][j] >= board[i][j]:
                        monotonicity_up += math.log2(board[i][j]) - math.log2(board[i-1][j])
                # check bottom tiles
                if i < 3:
                    if board[i+1][j] == 0:
                        monotonicity_down += math.log2(board[i][j])
                    elif board[i+1][j] >= board[i][j]:
                        monotonicity_down += math.log2(board[i][j]) - math.log2(board[i+1][j])
    return max(monotonicity_left, monotonicity_right, monotonicity_up, monotonicity_down)

def get_heuristic_score(move, board):
    new_board = execute_move(move, board)
    return 0.1 * sum_of_tile_values(new_board) + 0.5 * smoothness(new_board) + 0.4 * monotonicity(new_board)

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
