# -*- coding: utf-8 -*-
"""

This code is from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case

"""
from utils.samppa_visualize import *

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
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


        #Samppa
        crnode = Node(current_node, (current_node.position[0], current_node.position[1]))
        # Found the goal
        if crnode == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        #Samppa
        old_position = (0,-1)
        ldir = (1,0)
        bdir = (0,1)

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            #Samppa
            if len(current_node.position) == 3:
                if current_node.position[2] == (1,0):
                    ldir =(0,1)
                if current_node.position[2] == (0,1):
                    ldir =(-1,0)
                if current_node.position[2] == (0,-1):
                    ldir =(1,0)
                if current_node.position[2] == (-1,0):
                    ldir =(0,-1)  
                bdir = (-current_node.position[2][0], -current_node.position[2][1])
            print("*", ldir)
            #Samppa: is not node on to the backward:
            
            # Get node position
            #Samppa if
            print(current_node.position)
            print(new_position == ldir, ldir)
         
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            #samppa
            node_position = (node_position[0], node_position[1], (new_position[0], new_position[1]))
            # Make sure within range
            if new_position == ldir:
                continue
            if new_position == bdir:
                continue
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            #node_position = (node_position[0], node_position[1], (new_position[0], new_position[1]))
            
            # Create new node
            new_node = Node(current_node, node_position)
            children.append(new_node)
            
                 

        # Loop through children
        for child in children:
            
            # Child is on the visited list (search entire visited list)
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and f cost is already lower
            if len([open_node for open_node in open_list if child == open_node and child.f > open_node.f]) > 0:
                continue

            # Add the child to the yet_to_visit list
            open_list.append(child)


def main():

    # The maze we are actually looking for the solution
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
    end1 = (11,2)

# Bit smaller maze but this one shows what can happen with the first move... Basically you could go to left or right first!
    maze2 = [[0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 1, 0],
             [0, 0, 0, 1, 0, 0]]

    start2 = (2, 1)
    end2 = (2, 4)

     # You could also test with this maze in the beginning and observe how the algorithms is working. 
    # Note, that here also, the first move can be taken to ANY (basically to right or left)
    #maze3 = [[0, 0, 0],
    #        [0, 1, 0],
    #        [0, 0, 0]]

    # start3 = (2, 1)
    # end3 = (0, 2)

    path = astar(maze1, start1, end1)
    print(path)
    print_maze(maze1, path)
    animate_maze(maze1, path)
if __name__ == '__main__':
    main()
