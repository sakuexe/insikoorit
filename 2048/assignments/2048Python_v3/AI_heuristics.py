import constants as c
import random
import logic

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}

def AI_play(matrix):
   
    #key = heuristic_random()
    key = heuristic_empty_tile(matrix)

    return key

def heuristic_random():
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    key=tmp[random.randint(0,3)]
    return key

def heuristic_empty_tile(matrix):
    best_score = -1
    return_key = None
    for key in commands.keys():
        game, done, points = commands[key](matrix)  

        if not done:
           pass

        if done:
            n_empty=0
            for i in range(c.GRID_LEN):
                for j in range(c.GRID_LEN):
                    if game[i][j]==0:
                        n_empty+=1
            if n_empty > best_score:
                best_score = n_empty
                return_key = key
           

    print("Best move seems to be: ")
    print(return_key)    

    return return_key

