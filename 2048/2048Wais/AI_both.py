import numpy as np
import copy
import constants as c
import logic
import AI_heuristics as h
from multiprocessing.pool import ThreadPool

pool = ThreadPool(4)
transposition_table = {}

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}

def AI_play(matrix, max_depth):
    
    bestscore=-1000000
    best_key=None
  
    for key in commands.keys():
        tmp_score = score_toplevel_move(key, matrix, max_depth)
        if tmp_score>bestscore:
            bestscore = tmp_score
            best_key = key

    return best_key


def score_toplevel_move(key, board, max_depth):
    """
    Entry Point to score the first move.
    """
    newboard = commands[key](board)[0]

    if board == newboard:
        return -1000000

    # With many empty tiles calculation of many nodes would take to long and not improve the selected move
    # Less empty tiles allow for a deeper search to find a better move
    if (max_depth == -1):
        empty_tiles = sum(sum(np.array(newboard)==0))

        if empty_tiles > 12:
            max_depth = 1
            
        elif empty_tiles > 7:
            max_depth = 2
            
        elif empty_tiles > 4:
            max_depth = 3
            
        elif empty_tiles >= 1:
            max_depth = 4
            
        elif empty_tiles >= 0:
            max_depth = 6
        else:
            max_depth = 2

    score = calculate_chance(newboard, 0, max_depth)
    return score



def calculate_chance(board, curr_depth, max_depth):
    if curr_depth >= max_depth:
        return h.heuristic_combined(board)
  
    possible_boards_2 = []
    possible_boards_4 = []

    for x in range(c.GRID_LEN):
        for y in range(c.GRID_LEN):
            if board[x][y] == 0:
                new_board = copy.deepcopy(board)
                new_board[x][y] = 2
                possible_boards_2.append(new_board)

                new_board = copy.deepcopy(board)
                new_board[x][y] = 4
                possible_boards_4.append(new_board)

    # Add your code here!!!
    # Calculate the expected score for boards with a '2' placed (90% spread over possible boards)
    if possible_boards_2:
        scores_2 = np.array([
            calculate_max(board, curr_depth + 1, max_depth)
            for board in possible_boards_2
        ])
        e_min = np.sum(scores_2 * (0.9 / len(possible_boards_2)))  # Multiply each score by its probability
    else:
        e_min = 0

    # Calculate the expected score for boards with a '4' placed (10% spread over possible boards)
    if possible_boards_4:
        scores_4 = np.array([
            calculate_max(board, curr_depth + 1, max_depth)
            for board in possible_boards_4
        ])
        e_max = np.sum(scores_4 * (0.1 / len(possible_boards_4)))  # Multiply each score by its probability
    else:
        e_max = 0

    # Return the total expected value by summing the weighted scores
    return e_min + e_max

def calculate_max(board, curr_depth, max_depth):
    if curr_depth >= max_depth:
        return h.heuristic_combined(board)

    best_score = 0
        
    for key in commands.keys():
        successor = commands[key](board)[0]
        if board==successor:
            continue
        score = calculate_chance(successor, curr_depth + 1, max_depth)
        if best_score < score:
            best_score = score

    return best_score

