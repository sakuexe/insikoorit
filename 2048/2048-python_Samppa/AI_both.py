import constants as c
import random
import AI_minimax
import AI_heuristics
import logic

global over
over = False
global inde1
inde1 = 0
global inde2
inde2 = 0
global maps
maps =[]
keys = []
global keys1
keys1 =[]
global GameOver
GameOver = False
tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
def AI_play(m):
    #key=tmp[random.randint(0,3)]
    global maps
    maps = m
    
    key, mv = look(m)
    
    #mv, done, points = AI_heuristics.commands[key](m) 
    
    #if stucked
    
    pp =0
    key2 = key

    key = key2
    
    empty = False
    zer = AI_heuristics.zero(mv)
    pp3, key3 = AI_heuristics.next_tile(maps, mv, key)
    while pp3==10000000 and key == key2:
        pp3, key3 = AI_heuristics.next_tile(maps, mv, key)
        key = key3
        zer = AI_heuristics.zero(mv)
        if zer == 0 and maps == mv:
            empty = True
        else:
            empty = False
    while empty:
        key, mv = look(mv)
        mv, done, points = AI_heuristics.commands[key](mv) 
        zer = AI_heuristics.zero(mv)
        if zer == 0 and maps == mv:
            empty = True
        else:
            empty = False
    print("Z", zer)
    print("¤", key)     
    if empty == False:
        global GameOver
        GameOver = True  
    return key
def look(m):
    print(over)
    global keys1
    keyolds  = keys1
    if over == False:    
        keys1 = make_keys(m)
        global inde2
        inde2 = 0
    mva = m
    key, m = read_keys(keys1,m)
    #if keys1 == keyolds and m == mva:
    #    global GameOver
    #    GameOver =  True 
    return key, m

def GameOv():
    return GameOver
def make_keys(m):
    keysor = keys1
    keys =[]
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
    #random initial directions
    #key=tmp[random.randint(0,3)]
    key = tmp[0]
    #k =tmp[random.randint(0,3)]
    k = tmp[1]
    map = m
    
    #print(keys)
    #key=tmp[random.randint(0,3)]
    
        #kmm = (AI_minimax.mima(m))
        #k = AI_heuristics.AI_play(m)

    sumheura=0
    m1 = m
    m2 = m
    keysa = []
    a = 0
    pka = 0
    
    for z in range(4):
            maks = 0
            for a in range(4):
                keymm = tmp[a]
                ck = keymm
                mo = m1
                m1, done, poi = AI_minimax.commands[AI_heuristics.AI_play(m1)](m1)
                pointsa, nk = AI_heuristics.AI_play2(mo, m1, keymm, ck) 
                
                #print("a", pointsa)    
            #print(points)
                if pointsa>maks:
                    maks = pointsa
                    k = keymm
                    if ck!=nk:
                        k =nk
                    #m3, done, pka =  AI_minimax.commands[k](m1)
                    pka = 10
                #print("a", k, pka, maks) 
            keysa.append(k)
            sumheura=sumheura+pka
            pka = 0
            print("h", sumheura, k)
        #k = AI_heuristics.AI_play(m1)
            #keysa.append(k)
                
    summ=0
    keysb =[]
    for v in range(4):
        m2, done, pointsb = AI_minimax.commands[AI_minimax.AI_play(m2)](m2)
        kmm = (AI_minimax.mima(m2))
        keysb.append(kmm)
        summ=summ+pointsb
        print("S", summ)
    #heuristcs 2 times more weight
    if sumheura*2> summ:
        keys = keysa
        mold = m1
        print("heu")
    else:
        keys = keysb
        mold =m2
        print("minimax")  
    print("*", keys)
    global over
    over = True
    #if same keys serie and map ->random
    if keys == keysor and mold == m:
        keys = rand_keys()
        print("random", keys)
    return keys
def rand_keys():
    keys =[]
    for r in range(4):
        keys.append(tmp[random.randint(0,3)])
    
    return keys

def read_keys(kes, mr):
    
    global inde2
    print(inde2)
    if inde2<4:
        key = kes[inde2]
        inde2 = inde2 +1
    if inde2 >= 4:
            inde2 = 0
            global over
            over = False
    
    print("!",key)
    
    #print("*", key, inde1, len(keys))
    keyser5, mv3 = AI_minimax.play3(mr)
    return key, mv3
"""
def mima(m):
    global inde2
    indx = inde2
    print(indx)
    cccc=c.KEY_LEFT
    keyser, m = AI_minimax.play3(m)
    if len(keyser)>0:
        #cccc = keyser[indx] 
        print("*", keyser)
        if indx < len(keyser):
            cccc = keyser[indx]
            print(cccc)
            indx = indx + 1
            if indx >= len(keyser) :
                indx = 0
        inde2 = indx
       
    return cccc
"""
