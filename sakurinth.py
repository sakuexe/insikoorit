# -*- coding: utf-8 -*-
"""
This code is from
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case
---
The maze can only be traversed with moving either up or right
"""


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        # y, x
        self.position = position

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
                path.append(current.position)
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
            if current_node.parent is None:
                current_direction = new_position
            else:
                current_direction = (current_node.position[0] - current_node.parent.position[0],
                                     current_node.position[1] - current_node.parent.position[1])

            if current_direction != new_position:
                # direction: right
                if current_direction == (0, 1) and new_position != (1, 0):
                    print(f"1. invalid move to position: \
                    {current_node.position}, \
                    from {current_node.parent.position}")
                    continue

                # direction: left
                elif current_direction == (0, -1) and new_position != (-1, 0):
                    print(f"2. invalid move to position: \
                    {current_node.position}, \
                    from {current_node.parent.position}")
                    continue

                # direction: down
                elif current_direction == (1, 0) and new_position != (0, -1):
                    print(f"3. invalid move to position: \
                    {current_node.position}, \
                    from {current_node.parent.position}")
                    continue

                # direction: up
                elif current_direction == (-1, 0) and new_position != (0, 1):
                    print("4. invalid move to position:",
                          f"{current_node.position}",
                          f"from {current_node.parent.position}")
                    continue

            if current_node.parent is not None:
                print(f"valid move from: {current_node.parent.position}",
                      f"to {current_node.position}")
                print("with direction: ", new_position)

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the visited list (search entire visited list)
            # if len([closed_child for closed_child in closed_list if closed_child == child]) > 1:
            # continue

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

        # log to file the current state of the maze
        maze[current_node.position[0]][current_node.position[1]] = "X"
        for row in maze:
            for col in row:
                print(col, end=" ")
            print("", end="\n")
        maze[current_node.position[0]][current_node.position[1]] = 0


def print_maze(maze, path, path_char="~"):
    for position in path:
        maze[position[0]][position[1]] = path_char

    # print the labyrinth in a nicer way
    for row in maze:
        for col in row:
            if col == 1:
                print("#", end=" ")
            elif col == 0:
                print(" ", end=" ")
            else:
                print(col, end=" ")
        print("", end="\n")


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
    try:
        print_maze(test_maze, test_path)
        print("= " * maze1[0].__len__())
        print_maze(maze1, path)
    except Exception as e:
        print("maze is fucked:", path)
        print(e)


if __name__ == '__main__':
    main()
