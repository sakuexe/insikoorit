import constants as c
import random
import logic
import time

commands = {
    c.KEY_UP: logic.up,
    c.KEY_DOWN: logic.down,
    c.KEY_LEFT: logic.left,
    c.KEY_RIGHT: logic.right,
}


class GameSquare:
    def __init__(self, number: int, cordinates: tuple[int, int]):
        self.number = number
        self.cordinates = cordinates

    def __str__(self):
        return f"Number: {self.number}, Cordinates: {self.cordinates}"


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
        scores[direction] = get_potential_score(game, 5, 0)

    key = max(scores, key=scores.get)
    # time.sleep(0.2)

    return key


def get_potential_score(matrix: list[list[int]], depth: int, score) -> int:
    if depth == 0:
        return score

    for command in commands.values():
        game, _, points = command(matrix)
        if game == matrix:
            continue
        potential_points = 0
        potential_points += 10 * heuristic_stacking(game)
        potential_points += 3 * heuristic_most_empty_places(game)
        potential_points += 2 * points
        score += potential_points * (depth * 50)

    return get_potential_score(matrix, depth - 1, score)


# return the biggest number and its cordinates
def get_numbers_in_order(matrix: list[list[int]]) -> list[GameSquare]:
    all_numbers = []
    for col in matrix:
        for square in col:
            currentSquare = GameSquare(square, (matrix.index(col), col.index(square)))
            all_numbers.append(currentSquare)

    # sort the numbers based on the number value
    all_numbers.sort(key=lambda x: x.number, reverse=True)
    return all_numbers


def heuristic_biggest_number_top_left(matrix: list[list[int]]) -> int:
    biggest_number_cordinates = get_numbers_in_order(matrix)[0].cordinates

    # make sure that the biggest number is in the bottom right corner
    return (biggest_number_cordinates[0] + biggest_number_cordinates[1])


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


def heuristic_stacking(matrix: list[list[int]]) -> int:
    score = 0
    biggest_squares = get_numbers_in_order(matrix)
    wanted_row = 0
    for index, square in enumerate(biggest_squares):
        if square.number == 0:
            continue
        # only check the first column to be okay
        if index + 1 == matrix[0].__len__():
            break
        diffX = square.cordinates[0] + index
        score += matrix[0].__len__() - diffX

        diffY = square.cordinates[1] + wanted_row
        score += matrix[0].__len__() - diffY
    return score
