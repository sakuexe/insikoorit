# -*- coding: utf-8 -*-
"""
This code is from
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case
---
The maze can only be traversed with moving either up or right
"""

import utils.visualize_maze as visualize
import argparse


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None):
        self.parent = parent
        # y, x
        self.position = position
        # self.direction = direction

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the
    given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    current_direction = (0, 0)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(
                    (current.position[0], current.position[1]))
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []

        # Adjacent squares
        for new_position in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            # Get node position
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1]
            )

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0:
                continue
            if node_position[1] > (len(maze[len(maze)-1]) - 1):
                continue
            if node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # get the direction of the first move
            current_direction = get_direction(current_node, new_position)

            if not is_valid_move(new_position, current_direction):
                continue

            # Create new node
            new_node = Node(current_node, node_position, new_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Create the f, g, and h values
            # g value is the travel cost from the start node to the current node
            child.g = current_node.g + 1
            # Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            # f value is the sum of g and h values
            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and f cost is already lower
            if len([open_node for open_node in open_list if child == open_node and child.f > open_node.f]) > 0:
                continue

            # Add the child to the yet_to_visit list
            open_list.append(child)


def get_direction(node, new_position: tuple[int, int]) -> tuple[int, int]:
    """Returns the current direction of the node based on it's last position"""
    if node.parent is None:
        return new_position

    yDirection = node.position[0] + node.parent.position[0]
    xDirection = node.position[1] + node.parent.position[1]

    return (yDirection, xDirection)


def is_valid_move(new_position: tuple[int, int],
                  direction: tuple[int, int]) -> bool:
    """Returns True if the position of the new_position parameter
    is either forward or to the right of the current direction"""
    # if the new position is keeping in the same direction
    # aka going forward
    if direction == new_position:
        return True

    # direction: right
    if direction == (0, 1) and new_position == (1, 0):
        return False
    # direction: left
    elif direction == (0, -1) and new_position == (-1, 0):
        return False
    # direction: down
    elif direction == (1, 0) and new_position == (0, -1):
        return False
    # direction: up
    elif direction == (-1, 0) and new_position == (0, 1):
        return False

    return True


def main():
    # The maze we are actually looking for the solution
    maze1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
             [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
             [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
             [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]]

    start1 = (11, 10)
    end1 = (11, 2)

    # Bit smaller maze but this one shows what can happen with the first move.
    # Basically you could go to left or right first!
    test_maze = [[0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0]]

    test_start = (2, 1)
    test_end = (2, 4)

    test_path = astar(test_maze, test_start, test_end)
    path = astar(maze1, start1, end1)
    if path is None or test_path is None:
        print("No solution found")
        return
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--animate", type=int, nargs='?', const=10,
                            help="Animate the maze by passing the fps")
        args = parser.parse_args()
        if not args.animate:
            visualize.print_maze(maze1, path)
            return

        # get the framerate if provided with the argument
        visualize.animate_maze(maze1, path, framerate=args.animate)

    except Exception as e:
        print("maze is fucked, lmao:", path)
        print(e)


if __name__ == '__main__':
    main()
