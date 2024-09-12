# -*- coding: utf-8 -*-
"""

This code is from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case

"""
import utils.visualize_maze as visualize

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None):
        self.parent = parent
        self.position = position
        self.direction = direction
        

        self.g = 0 # cost to reach node
        self.h = 0 # estimated cost to goal
        self.f = 0 # sum

    # def compare(self, other):

    #     return self.position == other.position and self.direction == other.direction
    
    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction



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

        # Print the current state of the maze
        print_maze(maze, open_list, closed_list)

              # Print current and end node info
        print(f"Current Node: {current_node.position}, End Node: {end_node.position}")
        
        # Found the goal
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        directions = get_allowed_directions(current_node.direction)
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        for direction in directions:
            # Get node position
            node_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position,direction=direction)

            # Append
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
       

def get_allowed_directions(current_direction):
    """Returns allowed directions based on the current direction"""
     
    # If there's no current direction (i.e., at the start node),
    # allow movement either to the right or Up.
    if current_direction is None:
        return [(0, 1), (-1, 0,),(1,0),(0,-1)]  # Right and Up

    # If the current direction is to the right (0, 1),
    # you can continue moving right or turn down.
    if current_direction == (0, 1):
        return [(0, 1), (1, 0)]  # Right and Down

    # If the current direction is down (1, 0),
    # you can continue moving down or turn left.
    if current_direction == (1, 0):
        return [(1, 0), (0, -1)]  # Down and Left

    # If the current direction is left (0, -1),
    # you can continue moving left or turn up.
    if current_direction == (0, -1):
        return [(0, -1), (-1, 0)]  # Left and Up

    # If the current direction is up (-1, 0),
    # you can continue moving up or turn right.
    if current_direction == (-1, 0):
        return [(-1, 0), (0, 1)]  # Up and Right


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
    end1 = (11, 2)

# Bit smaller maze but this one shows what can happen with the first move... Basically you could go to left or right first!
    maze2 = [[0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 1, 0],
             [0, 0, 0, 1, 0, 0]]

    start2 = (2, 1)
    end2 = (2, 4)

    #  You could also test with this maze in the beginning and observe how the algorithms is working. 
    # Note, that here also, the first move can be taken to ANY (basically to right or left)
    maze3 = [[0, 0, 0],
           [0, 1, 0],
           [0, 0, 0]]

    start3 = (2, 1)
    end3 = (0, 2)

    path = astar(maze1, start1, end1)
    print(path)
    visualize.print_maze(maze1,path,"x")
    visualize.animate_maze(maze1,path)



if __name__ == '__main__':
    main()import utils.visualize_maze as visualize
