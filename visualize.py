import os
from time import sleep
from collections.abc import Iterable


DIRECTION_CHARS = {
    (0, 1): "→",
    (0, -1): "←",
    (1, 0): "↓",
    (-1, 0): "↑"
}


class Style:
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    GRAY = "\033[37m"
    RESET = "\033[0m"


def print_maze(maze: list[list[int]],
               path: Iterable[tuple],
               default_path_char="*",
               nav_color=Style.GREEN) -> None:
    """Prints the maze with the path visualized"""
    for position in path:
            y, x = position[0], position[1]
            direction = (0, 0)
            if position.__len__() == 3:
                direction = position[2]
            maze[y][x] = DIRECTION_CHARS.get(direction, default_path_char)
        
    # print the labyrinth in a nicer way
    print("=" * (maze[0].__len__() * 2 + 2))
    for row in maze:
        print(f"|{Style.GRAY}", end="")
        for col in row:
            if col == 1:
                print("#", end=" ")
            elif col == 0:
                print(" ", end=" ")
            else:
                print(f"{nav_color}{col}{Style.GRAY}", end=" ")
        print(f"{Style.RESET}|", end="\n")
    print("=" * (maze[0].__len__() * 2 + 2))


def animate_maze(maze: list[list[int]],
                 path: Iterable[tuple],
                 framerate=10,
                 default_path_char="*",
                 nav_color=Style.GREEN) -> None:
    """Animates the maze's progress with the path visualized"""

    if framerate <= 0:
        framerate = 1

    for position in path:
        y, x = position[0], position[1]
        direction = (0, 0)
        if position.__len__() == 3:
            direction = position[2]
        maze[y][x] = DIRECTION_CHARS.get(direction, default_path_char)

        print("=" * (maze[0].__len__() * 2 + 2))
        for row in maze:
            print(f"|{Style.GRAY}", end="")
            for col in row:
                if col == 1:
                    print("#", end=" ")
                elif col == 0:
                    print(" ", end=" ")
                else:
                    print(f"{nav_color}{col}{Style.GRAY}", end=" ")
            print(f"{Style.RESET}|", end="\n")
        maze[position[0]][position[1]] = " "
        print("=" * (maze[0].__len__() * 2 + 2))

        sleep(1 / framerate)
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    print("This is a module for visualizing the maze and the path.")
    print("Please import this module to use it.")