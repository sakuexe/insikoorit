import constants as c
import random
import logic

commands = {
    c.KEY_UP: logic.up,
    c.KEY_DOWN: logic.down,
    c.KEY_LEFT: logic.left,
    c.KEY_RIGHT: logic.right
}

def AI_play(matrix):
    scores = {
        c.KEY_UP: 0,
        c.KEY_DOWN: 0,
        c.KEY_LEFT: 0,
        c.KEY_RIGHT: 0
    }

    for direction, command in commands.items():
        game, done, points = command(matrix)
        if game == matrix:
            scores[direction] = 0
            continue
        
        #tempScore = 
        tempScore = 3 * heuristic_empty_tiles(game)
        tempScore += heuristic_biggest_tile_down_right(game)  # Suurimman palikan siirtäminen oikealle alas

        scores[direction] = tempScore
    
    key = max(scores, key=scores.get)  # Valitaan paras suunta
    return key

def heuristic_biggest_tile_down_right(matrix):
    biggest_tile = 0
    biggest_tile_position = (0,0)

    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN):
            if matrix[i][j] > biggest_tile:
                biggest_tile = matrix[i][j]
                biggest_tile_position = (i,j)

    row, col = biggest_tile_position
    score = 0

    # Palkitaan, jos suurin palikka on oikealla alhaalla
    if row == c.GRID_LEN - 1 and col == c.GRID_LEN - 1:
        score += 1000  # Palkitaan voimakkaasti, jos palikka on oikeassa alakulmassa
    
    # Palkitaan, jos suurin palikka on oikealla
    if col == c.GRID_LEN - 1:
        score += 500
    
    # Palkitaan, jos suurin palikka on alhaalla
    if row == c.GRID_LEN - 1:
        score += 500

    # Rankaiseminen, jos suurin palikka on kaukana oikeasta alakulmasta
    distance_from_bottom_right = abs(row - (c.GRID_LEN - 1)) + abs(col - (c.GRID_LEN - 1))
    score -= distance_from_bottom_right * 100  # Rankaise etäisyyden mukaan

    return score

def heuristic_empty_tiles(matrix):
    empty_tile = 0
    for row in matrix:
        empty_tile += row.count(0)
    
    return empty_tile 
