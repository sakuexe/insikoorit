import constants as c
import random
import logic
import AI_heuristics as AI
import AI_both
import numpy as np

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}
global indx
indx = 0
global keyser 
global tmp
tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 

def AI_play(matri):
    global tmp
    #random.shuffle(tmp)
    matrixi = matri
    
    
    global indx
    if indx == 0:
        global keyser
        keyser, matri = play3(matri)
    #print(indx)
    key = mima(matri)
    #random.shuffle(tmp)
    
    if (matrixi == matri):
        #print("#")
        
        for o in tmp:
            matri, done, point = commands[o](matri)
            if (point!=0):
                key = o
                break
       
        tmp2 = tmp
        c = 0
        random.shuffle(tmp2)
        co = tmp2[0]
        matri, done, point = commands[co](matri)
        while (point==0 and matri ==matrixi) and c<16:
            random.shuffle(tmp2)
            co = tmp2[0]
            matri, done, point = commands[co](matri)
            c=c+1
            key = co
        keyser, matri = play3(matri)
        indx = 0
    #print(key)
    return key
def play3(matri):
    lll = []
    for l in range(4):
        for keyt in tmp:
            #print(commands[keyt])
            matrit, done, point = commands[keyt](matri)
            ll,matrit = play3b(matrit)
            lll = lll +ll
    #print(lll)
    return lll, matrit
def play3b(matri):
    fff = []
    for x in range(4):
        #key=tmp[random.randint(0,3)]
        a = 0
        points = 0
        maks = 0
        ccc = []
        done = False
        points = [0,0,0,0]

        matrin = matri
        
        matrix1 = matri
        """
        for v in range(4):
            for u in range(4):
        """
        matrixb =[]
        #random.shuffle(tmp)
        points =[0,0,0,0]
        matrixnoa = [matri]
        matrixnob = [matri]
        matrixnoc = [matri]
        matrixnod = [matri]
        matrixs = matrix1
        
        a=0
        mak = 0 
        cou = 0
        points = [0,0,0,0]
        for y in range(8):
           
            for z in range(4):

                keymm = tmp[a]
                #print("!",commands[keymm])
                #print("MM", matrix1)
                matrin = matrix1
                matrix1, done, point = commands[keymm](matrixs)
                #print(point)
                if point>=mak:
                    mak = point
                    keyo = keymm
                   
                    points[a] = points[a] + point
                    
                    match a:
                        case 0:
                            matrixnoa.append(matrix1)
                        case 1:
                            matrixnob.append(matrix1)
                        case 2:
                            matrixnoc.append(matrix1)
                        case 3:
                            matrixnod.append(matrix1)
                
                a= a +1
                if a==4:
                    a=0
                match a:
                    case 0:
                        if (len(matrixnoa)>0):
                            matrix1 = matrixnoa
                    case 1:
                        if (len(matrixnob)>0):
                            matrix1 = matrixnob
                    case 2:
                        if (len(matrixnoc)>0):
                            matrix1 = matrixnoc
                    case 3:
                        if (len(matrixnod)>0):
                            matrix1 = matrixnod
                if (len(matrixs)>4):
                    matrixs = matrix1.pop(0)
                
                
        ma = 0
        f = 0
     
        for q in range(4):    
          if points[q]>ma:
            ma = points[q]
            f = q
                
        ccc.append(keyo)
        
   
    return ccc, matrin
def mima(m):
    #indx = AI_both.inde1
    cccc=c.KEY_LEFT
    global indx
   
    if len(keyser)>0:
        if indx >= len(keyser):
            indx = 0
        cccc = keyser[indx] 
        
        #rint(indx)
        
        if indx < len(keyser):
            cccc = keyser[indx]
            
            indx = indx + 1
        if indx==4:
            indx = 0
    #print("C", cccc)
    return cccc
