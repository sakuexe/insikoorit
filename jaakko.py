# -*- coding: utf-8 -*-
"""

This code is from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case

"""
import utils.jaakko_visualize_maze as visualize


ANY, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4

Allowed_moves_for_direction = {ANY : [(-1, 0), (0, 1), (1, 0), (0, -1)],
                               UP: [(-1, 0), (0, 1)],
                               RIGHT: [(0, 1), (1, 0)],
                               DOWN: [(1, 0), (0, -1)],
                               LEFT: [(0, -1), (-1, 0)]}
Direction_map = {(-1, 0) : UP,
                 (0, 1) : RIGHT,
                 (1, 0) : DOWN,
                 (0, -1) : LEFT}
                 

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        # Edellinen "ruutu"
        self.parent = parent
        # Nykyinen ruutu
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    #
    # Löydetty, mutta tutikattomat solmut
    open_list = []
    # Solmut jotka on tutkittu
    closed_list = []
    # Add the start node
    open_list.append(start_node)

    # Aloitus suunta on ylöspäin
    current_direction = UP
    
    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        #
        # Alustetaan nykyinen solmu avoimesta listasta
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        #
        # Poistetaan solmu avoimesta listasta (tutkimattomat)
        open_list.pop(current_index)
        # Lisää solmun suljettuun listaan (tutkitut)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        #
        # sisältää kaikki mahdolliset seuraavat solmut,
        # joihin voidaan siirtyä nykyisestä solmusta
        children = []
        allowed_moves = Allowed_moves_for_direction[current_direction]
        for move in allowed_moves:
            new_position = (current_node.position[0] + move[0], # X-koordinaatti
                            current_node.position[1] + move[1]) # Y-koordinaatti

            # Tarkastetaan onko sijainti labyrinthin sisällä.
            if (new_position[0] < 0 or new_position[0] >= len(maze) or
                    new_position[1] < 0 or new_position[1] >= len(maze[0])):
                continue
            
            # Tarkastetaan onhan sijainti labyrintissä kuljettavissa.
            if maze[new_position[0]][new_position[1]] != 0:
                continue

            new_node = Node(current_node, new_position)
            children.append(new_node)
        
        # Etsi lapsia käydyistä nodeista
        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child == open_node and child.f > open_node.f]) > 0:
                continue

            open_list.append(child)

        # Update current direction
        if children:
            next_move = (children[0].position[0] - current_node.position[0],
                         children[0].position[1] - current_node.position[1])
            current_direction = Direction_map[next_move]

    return None


def print_maze(maze, open_list, closed_list, path=[]):
    """Prints the maze with open list 'O', closed list 'C', and path 'X'"""
    maze_copy = [row[:] for row in maze]
    
    for node in open_list:
        x, y = node.position
        maze_copy[x][y] = 'O'  # Mark open list nodes with 'O'
    
    for node in closed_list:
        x, y = node.position
        maze_copy[x][y] = 'C'  # Mark closed list nodes with 'C'
    
    for position in path:
        x, y = position
        maze_copy[x][y] = 'X'  # Mark the path with 'X'
    
    for row in maze_copy:
        print(" ".join(str(cell) for cell in row))
    print("\n" + "-"*20 + "\n")

def main():

    maze1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0 ,1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0 ,1, 1, 1, 1, 1, 0, 1, 0],
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

    maze2 = [[0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 1, 0],
             [0, 0, 0, 1, 0, 0]]

    start2 = (0, 2)
    end2 = (2, 5)

    maze3 = [[0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]]

    start3 = (0, 0)
    end3 = (2, 2)

    path = astar(maze2, start2, end2)
    print(path)
    visualize.print_maze(maze2,path,"x")
    visualize.animate_maze(maze2,path)

if __name__ == '__main__':
    main()