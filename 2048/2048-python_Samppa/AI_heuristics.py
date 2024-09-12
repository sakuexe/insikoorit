import constants as c
import random
import logic

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}

def AI_play(matrix):
    #Samppa
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
    #Samppa         
    key = c.KEY_LEFT
    maxp = 0
    
    #matrix3, done, points = self.commands[key](self.matrix)
    #N = max number of tries Samppa
    
    for k in range(4):
            #N = 0
            #tried = tmp
            
            #while tried != [0,0,0,0] and N <8600:
            #    N = N + 1
                #print(N)
                #ADDED matrix3, self.matrix (matrix3 result of a tryed key Samppa
        matrix3, done, points = commands[key](matrix) 
        #if tried[k]!=0:           
        po = AI_play2(matrix, matrix3, k, key)
        if po > maxp:
            key = tmp[k]
            maxp = po
            #print("*", po, key)
                #tried[k] = 0
        """
        else:
            for i in range (4):
                if tried[i] != 0:
                    key = tried[i]
        """
        """debug
        print (tried)
        print(key, maxp)
        """
        #print("!", self.matrix, matrix3)
        #if matrix == matrix3:
        #    tried[k] = 0
        #key = heuristic_random()
        
        key2, po_empty = heuristic_empty_tile(matrix)
      
        if (po_empty*maxp /5)>maxp:
            key = key2
            #Samppa 
    print(po_empty*maxp /5, key, maxp)
    return key
   
def AI_play2(matror, matr, k1, key1):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    #key=tmp[random.randint(0,3)]
    #Samppa
    #And points plus 1 as a base Samppa 
    pointsM = 1
    k = tmp[k1]
    #multiplyer 20 if up left corner has something
    pointsM = pointsM + 200 * up_left_max(matr)
    #multiplyer 10 if down right corner has something  
    pointsM = pointsM + 100 * down_right_max(matr)  
    #multiplyer 5 if down left corner has something
    pointsM = pointsM + 50 * down_left_max(matr)
    #multiplyer 3 if up right corner has something  
    pointsM = pointsM + 30 * up_right_max(matr) 
    #sum of differences
    pointsM = pointsM + 30 * summa (matr)
    #if full points are 0
    pointsM = pointsM + 1000 * full(matr)
    #print key in loop and its value 
    #print("*", k, pointsM)
    return pointsM

def up_left_max(mat):
    #print(mat[0][0])
    return mat[0][0]
def down_right_max(mat):
    return mat[3][3]
def down_left_max(mat):
    #print(mat[0][0])
    return mat[0][3]
def up_right_max(mat):
    return mat[3][0]
def summa (m2):
    s = 0
    for x in range(3):
        for y in range(3):
            s = s + m2[x][y]*50
    #print ("sum", s)
    return s
def full(mf):
    flag = False
    for x in range(3):
        for y in range(3):
            if mf[x][y] != 0:
                flag = True
    if flag:
        return 1
    else:
        return 0
   


    
"""
def heuristic_random():
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    key=tmp[random.randint(0,3)]
    return key
"""
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
           

    #print("Best move seems to be: ")
    
    #print(return_key)    

    return return_key, n_empty

