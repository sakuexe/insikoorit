import numpy as np
import constants as c
import random
import logic

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}

# Note! depth has no effect for pure heuristic version!!
def AI_play(matrix, depth):
   
    #key = heuristic_random()
    key = heuristic_empty_tile(matrix)

    return key

def heuristic_random():
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    key=tmp[random.randint(0,3)]
    return key

def heuristic_empty_tile(matrix):
    best_score = -1
    return_key = None
    
    for key in commands.keys():
        game, done, points = commands[key](matrix)  

        if not done:
           pass

        if done:
            n_empty=n_empty_tiles(game)
            if n_empty > best_score:
                best_score = n_empty
                return_key = key

    return return_key

# Aseta isoin kulmaan
# täytä rivi
# vältä alas liikettä
# yhdistä isot


def corner():
    pass


def biggest_tiles_locations(matrix):
    tilesdict = {}

    matrix_columns = len(matrix)
    matrix_rows = len(matrix[0])

    for x in range(matrix_columns):
        for y in range(matrix_rows):
            tilesdict[x, y] = matrix[x][y]


    max_value = max(tilesdict.values())
    
    
    max_dict = {key: value for key, value in tilesdict.items() if value == max_value}
        
    return max_dict

    
def biggest_tile(matrix):
    biggest = -1

    for x in matrix:
        if max(x) > biggest:
            biggest = max(x)

def biggest_in_corner(matrix, biggest_tile: int):
    if matrix[0][0] == biggest_tile or matrix[0][3] == biggest_tile:
        return True
    return False


def first_row_full(matrix):
    if 0 in matrix[0]:
        return False
    return True

def safe_moves(setup1: bool, setup2: bool, setup3: bool):
    # Ylärivi täyden mukaan anna sopivat liikkeet
    if setup == True:
        return [c.KEY_UP, c.KEY_RIGHT, c.KEY_LEFT] 

    return [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 

    




def n_empty_tiles(matrix):       
    return sum(sum(np.array(matrix)==0))
