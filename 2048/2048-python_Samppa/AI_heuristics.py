import constants as c
import random


def AI_play(puz, matrix):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
    #Samppa         
    key = c.KEY_LEFT
    maxp = 0
    
    #matrix3, done, points = self.commands[key](self.matrix)
    #N = max number of tries Samppa
    
    for k in range(4):
        N = 0
        tried = tmp
        GO = False
        while tried != [0,0,0,0] and N <8600:
            N = N + 1
            #print(N)
            #ADDED matrix3, self.matrix (matrix3 result of a tryed key Samppa
            matrix3, done, points = puz.commands[key](matrix) 
            if tried[k]!=0:           
                po = AI_play2(matrix, matrix3, k, key)
                if po > maxp:
                    key = tmp[k]
                    maxp = po
                    #tried[k] = 0
            else:
                for i in range (4):
                    if tried[i] != 0:
                        key = tried[i]
            """debug
            print (tried)
            print(key, maxp)
            """
            #print("!", self.matrix, matrix3)
            if matrix == matrix3:
                tried[k] = 0
        if matrix == matrix3:
            GO = True
            for a in range(2):
                """
                k=k+1
                if k > 3:
                    k = 1
                """
                ke = tmp[a+1]
                if ke == 0:
                    ke = 'Down'
                print(a, ke)
                matrix2, done, points = puz.commands[ke](matrix) 
                if matrix2 != matrix:
                    GO = False
                key = ke
    return key, GO
    """        
            #tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
            #key=tmp[random.randint(0,3)]
            #commented Samppa
            #self.commands[key](self.matrix)
            #Samppa
            matrix2=self.matrix
            # ORIGINAL
            self.matrix, done, points = self.commands[key](self.matrix)
            #ORIGINAL
            self.points += points
            #Samppa
            print("#", done)
            GS = 'Not'
            if self.matrix == matrix2: 
                self.game_over = True
                done = True
                GS = 'lose'
                print(GS)
    """        
def AI_play2(matror, matr, k1, key1):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    #key=tmp[random.randint(0,3)]
    #Samppa
    #And points plus 1 as a base Samppa 
    pointsM = 1
    k = tmp[k1]
    #multiplyer 20 if up left corner has something
    pointsM = pointsM + 20 * up_left_max(matr)
    #multiplyer 10 if down right corner has something  
    pointsM = pointsM + 10 * down_right_max(matr)  
    #multiplyer 5 if down left corner has something
    pointsM = pointsM + 5 * down_left_max(matr)
    #multiplyer 3 if up right corner has something  
    pointsM = pointsM + 3 * up_right_max(matr) 
    #sum of differences
    pointsM = pointsM + 3 * summa (matr)
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
   
