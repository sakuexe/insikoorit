import constants as c
import random
import logic

commands = {
    c.KEY_UP: logic.up,
    c.KEY_DOWN: logic.down,
    c.KEY_LEFT: logic.left,
    c.KEY_RIGHT: logic.right,
}


def AI_play(matrix):
    scores = {
        c.KEY_UP: 0,
        c.KEY_DOWN: 0,
        c.KEY_LEFT: 0,
        c.KEY_RIGHT: 0,
    }

    for [direction, command] in commands.items():
        game, done, points = command(matrix)
        if game == matrix:
            scores[direction] = 0
            continue
        potential_score = 5 * heuristic_biggest_number_top_left(game)
        potential_score += 2 * points
        # potential_score += 7 * heuristic_most_points(game)
        potential_score += 5 * heuristic_most_empty_places(game)
        # don't lose, stupid
        potential_score *= 0 if logic.game_state(game) == "lose" else 1
        scores[direction] = potential_score

    key = max(scores, key=scores.get)

    return key


# return the biggest number and its cordinates
def get_biggest_number(matrix: list[list[int]]) -> tuple[int, tuple[int, int]]:
    biggest_number = 0
    biggest_number_cordinates = (0, 0)
    for col in matrix:
        for square in col:
            if square > biggest_number:
                biggest_number = square
                biggest_number_cordinates = (
                    matrix.index(col), col.index(square))

    return biggest_number, biggest_number_cordinates


def heuristic_biggest_number_top_left(matrix: list[list[int]]) -> int:
    biggest_number = 0

    number, biggest_number_cordinates = get_biggest_number(matrix)
    biggest_number = max(biggest_number, number)

    # count the difference between the biggest number cords
    # and the top left corner
    diff_x = matrix[0].__len__() - biggest_number_cordinates[0]
    diff_y = matrix[0].__len__() - biggest_number_cordinates[1]
    return (diff_x + diff_y)


def heuristic_most_points(matrix: list[list[int]]) -> int:
    points = 0
    for col in matrix:
        for square in col:
            points += square
    return points


def heuristic_most_empty_places(matrix: list[list[int]]) -> int:
    empty_places = 0
    for col in matrix:
        for square in col:
            if square == 0:
                empty_places += 1
    return empty_places
