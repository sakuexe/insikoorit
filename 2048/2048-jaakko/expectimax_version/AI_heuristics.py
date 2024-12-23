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

def n_empty_tiles(matrix):       
    return sum(sum(np.array(matrix)==0))

def heuristic_biggest_tile_down_right(matrix):
    biggest_tile = 0
    biggest_tile_position = (0,0)

    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN):
            if matrix[i][j] > biggest_tile:
                biggest_tile = matrix[i][j]
                biggest_tile_position = (i,j)

    rivi, sarake = biggest_tile_position
    score = 0

    # Jos oikeassa alakulmassa
    if rivi == 3 and sarake == 3:
        score += 25
    # Jos oikealla
    if sarake == 3:
        score += 5
    # Jos alhaalla
    if rivi == 3:
        score += 5

    # Rankaiseminen, jos suurin palikka on kaukana oikeasta alakulmasta
    # abs = absoluuttinen arvo
    matkaOikealtaAlhaalta = abs(rivi - 3) + abs(sarake - 3)
    score -= matkaOikealtaAlhaalta * 10

    return score
