import constants as c
import random
import logic

# TO DO
# 
# heuristiikka: katso mistä suunnasta saa eniten pisteitä !!!
# Jos ei muita suuntia valittavissa, valitse se ainoa (vaikka pisteet olisi 0) !
#
# looppaa peli useasti (100 kertaa?) 




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


    # matrix = laudan perustilanne enne siirtoa
    # game = laudan uusi mahdollinen siirto
    # done = ei tarpeellinen

    for direction, command in commands.items():
        game, done, points = command(matrix)
        # Jos siirto on turha, eli pelitilanne ei muutu
        if game == matrix:
            scores[direction] = 0
            continue
        
        tempScore = 10 * heuristic_empty_tiles(game)
        tempScore += heuristic_biggest_tile_down_right(game)  # Suurimman palikan siirtäminen oikealle alas

        scores[direction] = tempScore
    
     # Jos ei yhtään validia siirtoa, valitse suunta, jossa on eniten pisteitä
    #if all(score == 0 for score in scores.values()):
    #    key = random.choice(list(commands.keys()))
    #else: 
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

def heuristic_empty_tiles(matrix):
    empty_tile = 0
    for row in matrix:
        empty_tile += row.count(0)
    
    return empty_tile 

#def heuristic_first_move(GameGrid)

#def heuristic_sum_tiles(matrix)

