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
        scores[direction] = get_potential_score(game, 3, 0)

    key = max(scores, key=scores.get)
    # time.sleep(0.2)

    return key


def get_potential_score(matrix: list[list[int]], depth: int, score) -> int:
    if depth == 0:
        return score

    best_score = 0
    best_direction = matrix

    for command in commands.values():
        game, _, points = command(matrix)
        if game == matrix:
            continue
        potential_points = 0
        potential_points += 10 * heuristic_stacking(game)
        potential_points += 3 * heuristic_most_empty_places(game)
        potential_points += 2 * points
        # dont lose, stupid
        potential_points *= 0 if logic.game_state(game) == "lose" else 1

        if best_score < potential_points:
            best_score = potential_points
            best_direction = game

    score += best_score * (depth * 5)
    return get_potential_score(best_direction, depth - 1, score)


# return the biggest number and its cordinates
def get_numbers_in_order(matrix: list[list[int]]) -> list[GameSquare]:
    all_numbers = []
    for col in matrix:
        for square in col:
            currentSquare = GameSquare(
                square, (matrix.index(col), col.index(square)))
            all_numbers.append(currentSquare)

    # sort the numbers based on the number value
    all_numbers.sort(key=lambda x: x.number, reverse=True)
    return all_numbers


def heuristic_biggest_number_top_left(matrix: list[list[int]]) -> int:
    biggest_number_cordinates = get_numbers_in_order(matrix)[0].cordinates

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


def heuristic_stacking(matrix: list[list[int]]) -> int:
    score = 0
    biggest_squares = get_numbers_in_order(matrix)
    wanted_cords = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
    ]

    for index, cord in enumerate(wanted_cords):
        current_square = biggest_squares[index]
        if current_square.number == 0:
            continue

        if current_square.cordinates == cord:
            score += 10 * current_square.number

        # the distance to the wanted cords
        diffY = abs(current_square.cordinates[0] - cord[0])
        score += (matrix[0].__len__() - diffY)

        diffX = abs(current_square.cordinates[1] - cord[1])
        score += (matrix[0].__len__() - diffX)

        if current_square.cordinates != cord:
            break
    return score
