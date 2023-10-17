import random
import game
import numpy as np
import sys


UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    """
    Find the best move for the next turn using the Expectimax algorithm with a depth limit of 2.
    """
    bestmove = -1
    move_args = [UP, DOWN, LEFT, RIGHT]
    
    result = [score_toplevel_move(i, board, 4) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return bestmove

def score_move(move, board):
    """
    Score a move based on the resulting board state.
    """
    newboard = execute_move(move, board)

    if board_equals(board, newboard):
        return 0

    # TODO: Implement the Expectimax Algorithm.
    # 1.) Start the recursion until it reaches a certain depth
    depth_limit = 3
    if depth_limit == 0:
        return heuristic_score(newboard)
    else:
        possible_moves = [UP, DOWN, LEFT, RIGHT]
        scores = []
        for move in possible_moves:
            score = score_move(move, newboard)
            scores.append(score)
        return max(scores)

def score_toplevel_move(move, board, depth):
    """
    Score a move based on the resulting board state using the Expectimax algorithm with a depth limit.
    """
    newboard = execute_move(move, board)

    if board_equals(board, newboard):
        return 0

    if depth == 0:
        return heuristic_score(newboard)
    else:
        possible_moves = [UP, DOWN, LEFT, RIGHT]
        scores = []
        for move in possible_moves:
            score = score_toplevel_move(move, newboard, depth-1)
            scores.append(score)
        return max(scores)
    
def heuristic_score(board):
    """
    Calculate the heuristic score for a board state.
    """
    # Score based on the number of empty cells
    empty_cells = len(np.where(board == 0)[0])
    empty_cells_score = empty_cells * 100

    # Score based on the value of the tiles
    tile_values = [2**i for i in range(1, 12)]
    tile_scores = [np.sum(board == v) * v for v in tile_values]
    tile_score = np.sum(tile_scores)

    # Score based on the smoothness of the board
    smoothness_score = 0
    for i in range(4):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] == board[i][j+1]:
                smoothness_score += 1
            if board[j][i] != 0 and board[j][i] == board[j+1][i]:
                smoothness_score += 1

    # Combine the scores
    score = empty_cells_score + tile_score + smoothness_score
    return score

def add_random_tile(board):
    empty_cells = list(zip(*np.where(board == 0)))
    if empty_cells:
        random_cell = random.choice(empty_cells)
        board[random_cell] = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% chance of 4
    return board


def execute_move(move, board):
    """
    Move and return the grid with a new random tile.
    """
    new_board = np.copy(board)
    
    if move == UP:
        new_board = game.merge_up(new_board)
    elif move == DOWN:
        new_board = game.merge_down(new_board)
    elif move == LEFT:
        new_board = game.merge_left(new_board)
    elif move == RIGHT:
        new_board = game.merge_right(new_board)
    else:
        sys.exit("No valid move")
    
    # Add a random tile after the move
    new_board = add_random_tile(new_board)
    
    return new_board
        
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  
