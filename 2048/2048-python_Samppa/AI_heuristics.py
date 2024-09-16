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
        po, nkey = AI_play2(matrix, matrix3, k, key)
        if po > maxp:
            key = tmp[k]
            maxp = po
            #print(nkey)
            key = nkey
            #print("*", po, key)
                #tried[k] = 0
       
        #print("!", self.matrix, matrix3)
        #if matrix == matrix3:
        #    tried[k] = 0
        #key = heuristic_random()
        #!!
        """
        key2, po_empty = heuristic_empty_tile(matrix)
        #20000
        if (po_empty*1000000)>maxp:
            #print("!", po_empty*1000000, key2)
            #maxp = po_empty * 300000
            key = key2
            #print("*")
       """
    #print(po)
    #print(key, nkey) 
    #print(key)
    #!!!
   
    return key
   
def AI_play2(matror, matr, k1, keyII):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    #key=tmp[random.randint(0,3)]
    #ready given heuristic empty_tile
    pointsM = 100000 * heuristic_empty_tile(matr)
    #And points plus 1 as a base Samppa 
    pointsM = 1
    k = tmp[k1]
    nk = keyII
    #multiplyer 200 if up left corner has something
    pointsM = pointsM + 60000 * up_left_max(matr)
    #multiplyer 100 if down right corner has something  
    pointsM = pointsM + 10000 * down_right_max(matr)
     #multiplyer 50 if down left corner has something  
    pointsM = pointsM + 5000 * down_left_max(matr)
    #multiplyer 30 if up right corner has something  
    pointsM = pointsM + 3000 * up_right_max(matr) 
    #sum of differences
    pointsM = pointsM + 300 * summa (matr)
    #if full points are 0
    pointsM = pointsM + 10 * zero(matr)
    #if same then +1000000
    po_next, nk = next_tile(matror, matr, keyII)
    pointsM = pointsM + po_next
    #print(pointsM)
    return pointsM, nk

def up_left_max(mat):
    #print(mat[0][0])
    #print("U", 60000 * mat[0][0])
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
    for x in range(4):
        for y in range(4):
            s = s + m2[x][y]*50
    #print ("sum", s)
    return s
def zero(mf):
    f = 0
    for x in range(4):
        for y in range(4):
            if mf[x][y] == 0:
                f=f+1
   # print("ZERO", f)
    return f
   
def next_tile(m, m3, key_new):
    poin = 0
    newkey = key_new
    co = c.KEY_UP
    tmp2 = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    co = key_new
    m3, done, points = commands[co](m)
    if m == m3:
        a = 0
        for kkk in reversed(range(4)):
            a = kkk + 1
            if a == 4:
                a = 0
            if tmp2[kkk] == key_new:
                #print("!!!", key_new, tmp2[a])
                if  key_new != tmp2[a]:
                    newkey = tmp2[a]
                    poin = 10000000
        #print(newkey)
    return poin, newkey
"""
def heuristic_random():
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    key=tmp[random.randint(0,3)]
    return key
"""
def heuristic_empty_tile(matrix):
    best_score = -1
    return_key = None
    #Samppa
    n_empty = 0
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

