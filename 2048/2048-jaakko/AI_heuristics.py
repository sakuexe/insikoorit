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
        # Jos siirto on turha, eli pelitilanne ei muutu
        if game == matrix:
            scores[direction] = 0
            continue
        
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

    rivi, sarake = biggest_tile_position
    score = 0

    # Jos oikeassa alakulmassa
    if rivi == 3 and sarake == 3:
        score += 1000
    # Jos oikealla
    if sarake == 3:
        score += 250
    # Jos alhaalla
    if rivi == 3:
        score += 250

    # Rankaiseminen, jos suurin palikka on kaukana oikeasta alakulmasta
    # abs = absoluuttinen arvo
    matkaOikealtaAlhaalta = abs(rivi - 3) + abs(sarake - 3)
    score -= matkaOikealtaAlhaalta * 100

    return score

def heuristic_empty_tiles(matrix):
    empty_tile = 0
    for row in matrix:
        empty_tile += row.count(0)
    
    return empty_tile 

#def heuristic_first_move(GameGrid)

#def heuristic_sum_tiles(matrix)

