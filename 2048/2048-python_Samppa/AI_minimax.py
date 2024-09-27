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
global indxi
indxi = 0
global indx
indx = 0
global keyser 
keyser = c.KEY_UP
global tmp
tmp = [c.KEY_UP,  c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT, ] 
#tmp shuffled ? True, dont, False, shuffle
global shuffled 
shuffled = False
def AI_play(matri):
    global shuffled
    if shuffled == False:
        global tmp
        random.shuffle(tmp)
        #print(shuffled, tmp)
        shuffled = True
    global keyser
    keyser = [tmp[0]]
    matrixi = matri
    global indx
    if indx == 0:
        keyser, matri = play3(matri)
    
    key = mima(matri)
    
    
    if (matrixi == matri):
        #print("#")
        for o in tmp:
            matri, done, point = commands[o](matri)
            if (point!=0):
                key = o
                break
        #if still stucks, random direction
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
    maksi = 0
    maksimatri = matri
    mm = matri
    
    keych = tmp[0]
    for l in range(4):
        a=0
        for keyt in tmp:
            #print(commands[keyt])
            matrit, done, point = commands[keyt](matri)
            ll, matriti= play3b(matri)
            if (point>=maksi):
                maksi= point
                keych = ll[a]
                
                maksimatri = matriti
       
        #print(matri)
        a=a+1
        if a == 4:
            a=0
        mm = maksimatri
        #print(keych, maksi)
        
        lll.append(keych)

    #print(lll)
    return lll, matriti
    
def play3b(matri):
    fff = []
    matrorg = [matri]
    matrcold = [matri]
    for x in range(2):
        #key=tmp[random.randint(0,3)]
        a = 0
        points = 0
        maks = 0
        ccc = []
        done = False
        points = [0,0,0,0]

        matrin = matri
        
        matrix1 = matri
        
        #random.shuffle(tmp)
        matriisi = [matri, matri, matri, matri]
        points =[0,0,0,0]
        matrixnoa = [matri]
        matrixnob = [matri]
        matrixnoc = [matri]
        matrixnod = [matri]
        matrixs = matrix1
        f =0
        a=0
        b=0
        mak = 0 
       
        points = [0,0,0,0]
        for y in range(16):
            
            for z in range(4):

                keymm = tmp[a]
                #print("!",commands[keymm])
                #print("MM", matrix1)
                #matrin = matrixs
                matrix1, done, point = commands[keymm](matrixs)
                #print(point)
                if point>=mak:
                    mak = point
                    #matrin = matrix1
                    #keyo = keymm       
                    points[a] = points[a] + point
                    
                    match a:
                        case 0:
                            matrixnoa = matrix1
                        case 1:
                            matrixnob = matrix1
                        case 2:
                            matrixnoc =matrix1
                        case 3:
                            matrixnod = matrix1
                
                    a= a +1
                    if a==4:
                        a=0
            
                
                    match a:
                        case 0:
                            if (len(matrixnoa)>0):
                                matrix1 = matrixnoa
                                matriisi[0]= matrix1
                        case 1:
                            if (len(matrixnob)>0):
                                matrix1 = matrixnob
                                matriisi[1]= matrix1
                        case 2:
                            if (len(matrixnoc)>0):
                                matrix1 = matrixnoc
                                matriisi[2]= matrix1
                        case 3:
                            if (len(matrixnod)>0):
                                matrix1 = matrixnod
                                matriisi[3]= matrix1
            
                    if (len(matrixs)>4):
                        matrixs = matrix1[a]
            
            bmak = 0
            f=0 
            for b in range(4):
                if points[b]>= bmak:
                    bmak = points[b]
                    f = b
            matrin = matriisi[f]
            keyo=tmp[f]
        #matrorg.append(matriisi)       
        
        ccc.append(keyo)
        #(matrin)
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
