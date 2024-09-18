import constants as c
import random
import logic
import AI_heuristics as AI
import AI_both

commands = {c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right}
global indx
indx = 0

key = c.KEY_LEFT
def AI_play(matri):
    key = mima(matri)
    return key
def play3(matri):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT] 
    #key=tmp[random.randint(0,3)]
    a = 0
    points = 0
    maks = 0
    ccc = []
    done = False
    matrixd1 = matri
    for x in range(4):
        for y in range(4):
            for z in range(4):
                keymm = tmp[a]
                a= a +1
                if a==4:
                    a=0
                #print(keymm)
                matrixd1, done, points = commands[keymm](matri)
                #print(points)
                if points>maks:
                    maks = points
                    ccc.append(keymm)
                    #print("*****")
    
    return ccc, matrixd1
def mima(m):
    #indx = AI_both.inde1
    
    cccc=c.KEY_LEFT
    keyser, m = play3(m)
    if len(keyser)>0:
        global indx
        if indx >= len(keyser):
                indx = 0
        cccc = keyser[indx] 
        
        #rint(indx)
        #print("*", keyser)
        if indx < len(keyser):
            cccc = keyser[indx]
            #print(cccc)
            indx = indx + 1
       
    return cccc
def GameOv():
    return False