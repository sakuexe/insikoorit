import constants as c
import random

def AI_play(GameGrid):

    # Analyze gameboard and figure out good move
    # figure out heuristic  value

    points_dict = {key: 0 for key in range(4)}

    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]

    for x in range(len(tmp)):
        points = 0

        tst = tmp[x]
        points = GameGrid.commands[tst](GameGrid.matrix)
        
        points_dict[x] = points[2]

    print(points_dict)
    
    if points_dict[0] == 0 and points_dict[1] == 0 and points_dict[2] == 0 and points_dict[3] == 0:
        key=tmp[random.randint(0,3)]
        return key

    max_key = max(points_dict, key=points_dict.get)
    key = tmp[max_key]

    return key
