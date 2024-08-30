import os
from time import sleep
from collections.abc import Iterable


DIRECTION_CHARS = {
    (0, 1): "→",
    (0, -1): "←",
    (1, 0): "↓",
    (-1, 0): "↑"
}


def print_maze(maze: list[list[int]],
               path: Iterable[tuple],
               default_path_char="*") -> None:
    """Prints the maze with the path visualized"""

    for position in path:
        y, x = position[0], position[1]
        direction = (0, 0)
        if position.__len__() == 3:
            direction = position
        maze[y][x] = DIRECTION_CHARS.get(direction, default_path_char)

    # print the labyrinth in a nicer way
    print("=" * (maze[0].__len__() * 2 + 2))
    for row in maze:
        print("|", end="")
        for col in row:
            if col == 1:
                print("#", end=" ")
            elif col == 0:
                print(" ", end=" ")
            else:
                print(col, end=" ")
        print("|", end="\n")
    print("=" * (maze[0].__len__() * 2 + 2))


def animate_maze(maze: list[list[int]],
                 path: Iterable[tuple],
                 framerate=10,
                 default_path_char="*") -> None:
    """Animates the maze's progress with the path visualized"""

    if framerate <= 0:
        framerate = 1

    for position in path:
        y, x = position[0], position[1]
        direction = (0, 0)
        if position.__len__() == 3:
            direction = position
        maze[y][x] = DIRECTION_CHARS.get(direction, default_path_char)

        print("=" * (maze[0].__len__() * 2 + 2))
        for row in maze:
            print("|", end="")
            for col in row:
                if col == 1:
                    print("#", end=" ")
                elif col == 0:
                    print(" ", end=" ")
                else:
                    print(col, end=" ")
            print("|", end="\n")
        maze[position[0]][position[1]] = " "
        print("=" * (maze[0].__len__() * 2 + 2))

        sleep(1 / framerate)
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    print("This is a module for visualizing the maze and the path.")
    print("Please import this module to use it.")
