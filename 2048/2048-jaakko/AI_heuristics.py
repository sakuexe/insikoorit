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

def AI_play(matrix, move_count):
    if move_count == 0:
        return c.KEY_RIGHT  # Pakotetaan ensimmäinen siirto oikealle
    elif move_count == 1:
        return c.KEY_DOWN  # Pakotetaan toinen siirto alas

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
        
        tempScore = 3 * heuristic_empty_tiles(game)
        tempScore += heuristic_check_best_direction_for_points(matrix)
        if best_direction is not None:
            return best_direction
        else:
            # Jos ei löydy parasta suuntaa, käytetään toista heuristiikkaa
            return heuristic_random()  # Tai jokin muu valinta
        tempScore += 5 * heuristic_biggest_tile_down_right(game)

        scores[direction] = tempScore


    
    key = max(scores, key=scores.get)  # Valitaan paras suunta
    return key

def heuristic_check_best_direction_for_points(matrix):
    # Alustetaan muuttuja parhaalle pistemäärälle ja parhaalle suunnalle
    best_points = -1
    best_direction = None
    
    # Käydään läpi jokainen mahdollinen siirtosuunta
    for direction, command in commands.items():
        # Tehdään siirto ja tallennetaan tulos: uusi pelitilanne, onko siirto tehty, saadut pisteet
        new_matrix, done, points = command(matrix)
        
        # Jos siirto on mahdollinen (eli se muuttaa pelitilannetta), tarkastellaan pisteitä
        if done:
            if points > best_points:
                best_points = points  # Päivitetään paras pistemäärä
                best_direction = direction  # Päivitetään paras suunta

    # Palautetaan suunta, joka tuotti parhaat pisteet
    return best_direction



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
        score += 100
    # Jos oikealla
    if sarake == 3:
        score += 25
    # Jos alhaalla
    if rivi == 3:
        score += 25

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

