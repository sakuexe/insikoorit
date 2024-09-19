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
    key = heuristic_random()
     #key = heuristic_empty_tile(matrix)

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



def own_heuristic(matrix, move_number: int, last_move: str):


    return_key = None

    #----------------------------
    # get top right biggest manually
    if move_number == 0:
        return_key = c.KEY_UP
        return return_key

    if move_number == 1:
        return_key = c.KEY_RIGHT
        return return_key

    #----------------------------------

    # unfortunate situation cases
    # could just scratch if happens mebe

    #left case DD
    if last_move == logic.left:
        return_key = commands[c.KEY_RIGHT]
        last_move = return_key
        return return_key

    #up case DD
    if last_move == logic.down:
        return_key = commands[c.KEY_DOWN]
        last_move = return_key
        return return_key
    
    #------------------------------------------------

    # actual heuristics


    if move_number > 1:
        print("ok huutista")
        tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
        return_key=tmp[random.randint(0,3)]
        return return_key


    


    pass


# täytä rivi
# Aseta isoin kulmaan
# vältä alas liikettä
# yhdistä isot



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

    return biggest

def biggest_in_right_corner(matrix, biggest_tile: int):
    if matrix[0][3] == biggest_tile:
        return True
    return False

def first_row_full(matrix):
    if 0 in matrix[0]:
        return False
    return True


# palauttaa false jos ylärivissä yhdistyksiä
# true jos ei oo
def first_row_combinations(matrix):
    hashmap = {}

    for x in matrix:
        for y in matrix:
            if y not in hashmap:
                hashmap[y] = 1
            else:
                return False
    
        return True

def first_row_right(matrix):
    if matrix[0][0] == matrix[0][1] or matrix[0][1] == matrix[0][2] or matrix[0][2] == matrix[0][3]:
        return True
    return False


#def n_empty_tiles(matrix):       
#    return sum(sum(np.array(matrix)==0))

def safe_moves(first_row: bool, biggest_in_corner: bool, first_row_right: bool):

    if first_row == True and biggest_in_corner == True and first_row_right == False:
        return {c.KEY_UP: logic.up,
            c.KEY_RIGHT: logic.right,
            c.KEY_LEFT: logic.left}

    if first_row == True and biggest_in_corner == True and first_row_right == True:
        return {c.KEY_UP: logic.up,
            c.KEY_RIGHT: logic.right}

    if first_row == False and biggest_in_corner == True and first_row_right == False:
                return {c.KEY_UP: logic.up,
            c.KEY_RIGHT: logic.right}

    return {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}


