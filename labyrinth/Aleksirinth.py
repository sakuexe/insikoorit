# -*- coding: utf-8 -*-
"""
This code is from
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case
"""

import utils.visualize_maze as visualize

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None):
        self.parent = parent
        self.position = position
        self.direction = direction

        self.g = 0  # Cost
        self.h = 0  # Estimated cost
        self.f = 0  # Sum


    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction



def astar_straight_right(maze, start, end):
    """Returns a list of tuples as a path from the given start to the
    given end in the given maze"""

    moves_map = {
        None : [(0, 1), (-1, 0,), (1, 0), (0, -1)], # Start
        (-1, 0) : [(-1, 0), (0, 1)], # Up -> Right
        (1, 0) : [(1, 0), (0, -1)], # Down -> Left
        (0, 1): [(0, 1), (1, 0)],  # Right -> Down
        (0, -1): [(0, -1), (-1, 0)],  # Left -> Up
    }

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
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []

        # Adjacent squares
        for direction in moves_map[current_node.direction]:

            # Get node position
            node_position = (
                current_node.position[0] + direction[0],
                current_node.position[1] + direction[1])


            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0:
                continue
            if node_position[1] > (len(maze[len(maze) - 1]) - 1):
                continue
            if node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position, direction = direction)

            # Append
            children.append(new_node)


        # Loop through children
        for child in children:

            # Child is on the visited list (search entire visited list)
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and f cost is already lower
            if len([open_node for open_node in open_list if child == open_node and child.f > open_node.f]) > 0:
                continue

            # Add the child to the yet_to_visit list
            open_list.append(child)




def main():


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

    path = astar_straight_right(maze1, start1, end1)
    visualize.print_maze(maze1,path,"-")
    visualize.animate_maze(maze1,path)


if __name__ == '__main__':
    main()

    # mene suoraan jos pääsee
    # tarkista onko ruudussa käyty tällä vedolla
    # jos on tarkista onko sama suunta ollut
    # jos sama, kokeile mennä oikealle,
    # jos ei pääse mene taaksepäin
    # jos pääsee tarkista onko ruudussa käyty tällä vedolla
    # jos on mene taaksepäin
