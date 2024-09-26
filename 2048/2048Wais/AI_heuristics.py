import numpy as np
import constants as c
import random
import logic

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}

def AI_play(matrix):
   
    #key = heuristic_random()
    # key = heuristic_empty_tile(matrix)
    # key = heuristic_snake_weight(matrix)
    key = heuristic_combined(matrix)

    return key

def create_snake_weight_matrix(size):
    weights = [3**3, 2**2, 1**1, 0**0,
               4**4,  5**5,  6**6, 7**7, 
               11*11,  10**10,  9**9,  8**8, 
               12**12,  13**13,  14**14,  15**15]
    weight_matrix = []
    index = 0
    for i in range(size):
        row = []
        for j in range(size):
            row.append(weights[index])
            index += 1
        weight_matrix.append(row)
    return weight_matrix

def snake_weight_heuristic(matrix):
    size = len(matrix)
    weight_matrix = create_snake_weight_matrix(size)
    score = 0
    for i in range(size):
        for j in range(size):
            score += matrix[i][j] * weight_matrix[i][j]
    return score

def heuristic_snake_weight(matrix):
    best_score = -float('inf')
    return_key = None
    for key in commands.keys():
         # Create a copy of the matrix to avoid modifying the real game state
        game_copy = [row[:] for row in matrix]
         # Apply the move
        game, done, points = commands[key](game_copy)

        if done:
            score = snake_weight_heuristic(game)
            if score > best_score:
                best_score = score
                return_key = key

    print("Best move based on snake weight heuristic seems to be: ")
    print(return_key)


    return return_key

def heuristic_empty_tile(matrix):
    # print(f"this is matrix {matrix}")
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, points = commands[key](matrix)  

        if not done:
           pass

        if done:
            n_empty=0
            for i in range(c.GRID_LEN):
                for j in range(c.GRID_LEN):
                    if game[i][j]==0:
                        n_empty+=1
            if n_empty > best_score:
                best_score = n_empty
                return_key = key
           

    print("Best move seems to be: ")
    print(return_key)   

    return return_key 

def heuristic_combined(matrix):
    """
    Combines the snake weight heuristic with the empty tile heuristic.
    Chooses the move that optimizes both.
    """
    best_score = -float('inf')  # Start with a very low score
    return_key = None

    for key in commands.keys():
        # Create a copy of the matrix to avoid modifying the real game state
        game_copy = [row[:] for row in matrix]

        # Apply the move and get the resulting state, whether the move was valid, and the points gained
        game, done, points = commands[key](game_copy)

        # Only consider valid moves
        if done:
            # Calculate score using the snake weight heuristic
            snake_score = snake_weight_heuristic(game)
            
            # Count the number of empty tiles
            n_empty = sum(1 for i in range(c.GRID_LEN) for j in range(c.GRID_LEN) if game[i][j] == 0)
            
            # Combine both heuristics (you can adjust weights for both)
            combined_score = 0.8 * snake_score + 0.2 * n_empty  # Simple sum (you can adjust this)

            # Select the move with the highest combined score
            if combined_score > best_score:
                best_score = combined_score
                return_key = key

    # print("Best move based on combined heuristic (snake + empty tiles) is:", return_key)
    return combined_score

def n_empty_tiles(matrix):       
    return sum(sum(np.array(matrix)==0))
