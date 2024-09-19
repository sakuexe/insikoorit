import numpy as np
import constants as c
import logic
# import time

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


def AI_play(matrix, depth: int) -> int:
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
    """Use recursion to make sure that you find the move
    with the highest potential for scoring points.

    @param matrix: The current game matrix
    @param depth: The max depth of the recursion (how many moves ahead)
    @param score: For keeping track of the potential score for the direction

    @return: The total potential score for the direction
    """

    # the base case for the recursion
    if depth == 0:
        return score

    best_score = 0
    best_direction = matrix

    for command in commands.values():
        game, _, points = command(matrix)
        # do not compute if the move did nothing to the game board
        if game == matrix:
            continue

        potential_points = 0
        potential_points += 0.25 * heuristic_stacking(game)
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
    """Get all the numbers on the board, ordered from biggest to smallest.
    Including the cordinates of the number.

    @param matrix: The game matrix
    @return: A list of GameSquare objects (number, cordinates)
    """
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
    """The heuristic for the AI to move the biggest number to the
    top left corner."""
    biggest_number_cordinates = get_numbers_in_order(matrix)[0].cordinates

    # count the difference between the biggest number cords
    # and the top left corner
    diff_x = matrix[0].__len__() - biggest_number_cordinates[0]
    diff_y = matrix[0].__len__() - biggest_number_cordinates[1]
    return (diff_x + diff_y)


def heuristic_most_empty_places(matrix: list[list[int]]) -> int:
    """The heuristic for the AI to move the squares in a way that
    it creates the most empty places on the board.
    """
    return sum(sum(np.array(matrix) == 0))


def heuristic_stacking(matrix: list[list[int]]) -> float:
    """The heuristic for the AI to stack the numbers in a way that
    the biggest numbers are on top and ordered from left to right.
    """
    score = 0
    biggest_squares = get_numbers_in_order(matrix)
    wanted_cords = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 3),
        (1, 2),
        (1, 1),
        (1, 0),
    ]

    for index, cord in enumerate(wanted_cords):
        current_square = biggest_squares[index]
        if current_square.number == 0:
            continue

        if current_square.number < 8:
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

    return score * 0.1


def heuristic_snakeing(matrix: list[list[int]]) -> int | float:
    biggest_squares = get_numbers_in_order(matrix)
    score = 0
    for row_index, row in enumerate(matrix):

        if row_index % 2 == 0:
            for col_index in range(len(row)):
                numbers_cords = biggest_squares[col_index +
                                                row_index].cordinates
                if (row_index, col_index) == numbers_cords:
                    score += 100
                else:
                    score += abs(numbers_cords[0] - row_index)
                    score += abs(numbers_cords[1] - col_index)
                    break
            continue

        for col_index in range(len(row) - 1, 0, -1):
            numbers_cords = biggest_squares[col_index + row_index].cordinates
            if (row_index, col_index) == numbers_cords:
                score += 100
            else:
                score += abs(numbers_cords[0] - row_index)
                score += abs(numbers_cords[1] - col_index)
                break

    print("score of snakeing:", score)
    return score
