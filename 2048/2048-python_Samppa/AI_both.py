import constants as c
import random
import AI_minimax
import AI_heuristics
import logic
import numpy as np

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

    
    
    empty = False
    zer = AI_heuristics.zero(mv)
    pp3, key3 = AI_heuristics.next_tile(maps, mv, key)
    while pp3==10000000 and key == key2:
        pp3, key3 = AI_heuristics.next_tile(maps, mv, key)
        mv, done, points = AI_heuristics.commands[key3](mv) 
        key = key3
        global over 
        over = False
        zer = AI_heuristics.zero(mv)
        if zer == 0 and maps == mv:
            empty = True
        else:
            empty = False
        while empty:
            over = False
            key, mv = look(mv)
            mv, done, points = AI_heuristics.commands[key](mv) 
            zer = AI_heuristics.zero(mv)
            if zer == 0 and maps == mv:
                empty = False
            else:
                empty = True
    #print("Z", zer)
    #print("¤", key)     
    if empty == False:
        global GameOver
        GameOver = True  
    return key
def look(m):
    #print(over)
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
    poicom1=0
    poicom2 = 0
    poicom12 = 0
    poicom22 = 0
    #print(keys)
    #key=tmp[random.randint(0,3)]
    
        #kmm = (AI_minimax.mima(m))
        #k = AI_heuristics.AI_play(m)
    keyssum1 = []
    keyssum2 = []
    sumheura=0
    summ = 0
    m1 = m
    m2 = m
    keysa = []
    keysb = []
    a = 0
    pka = 0
    keysy = []
    keysz = []
    versum = 0
    versum2 =0 
    mold2 = m
    m3 = m
    m2 = m
    first = True
    N = 0
    a = 0
    for l in range (3):
       
        for z in range(2):
                maks = 0
                for a in range(4):
                    keymm = tmp[a]
                    ck = keymm
                    mo = m1
                    kh = AI_heuristics.AI_play(m3)
                    m1, done, pointsa = AI_heuristics.commands[kh](m3)
                    poi, nk = AI_heuristics.AI_play2(mo, m1, keymm, ck) 
                    
                    #print("a", pointsa)    
                #print(points)
                    pka = 0
                    if pointsa>=maks:
                        maks = pointsa
                        k = keymm
                        if ck!=nk:
                            k =nk
                        #m3, done, pka =  AI_minimax.commands[k](m1)
                        #WEIGHT of heuristics
                        pka = 3
                        N = a
                    #print("a", k, pka, maks) 
                sumheura=sumheura+pka
                keysa.append(k)
                
                #sumheura=sumheura+pointsa
                pka = 0
                #print("h", sumheura, k)
            #k = AI_heuristics.AI_play(m1)
                #keysa.append(k)
                    
        summ=0
        keysb =[]
        for v in range(2):
            km = AI_minimax.AI_play(m2)
            m2, done, pointsb = AI_minimax.commands[km](m2)
            kmm = (AI_minimax.mima(m2))
               #!!!! strategies have different first step
            #print("1", kmm, k, N)
            N = tmp.index(kmm)
            if kmm == k and first==True:
                N = N + 1
                if N == 4:
                    N = 0
                kmm = tmp[N]
            #print("2", kmm, k, N, first)
            first = False
            keysb.append(kmm)
            summ=summ+pointsb
            versum = versum + sumheura
            #print("S", summ)
        #heuristcs 2 times more weight
        if sumheura> summ:
            keysz.append(keysb)
            keysy.append(keysa)
            mold = m3
            #print("heu")
            versum = versum + sumheura
            versum2 = versum2 +summ
            #print(keysy)
        else:
            keysz.append(keysa)
            keysy.append(keysb)
            mold =m2
            #print("minimax")  
            versum = versum + summ
            versum2 = versum2 + sumheura
        #print("Y", keysy)
        #print("Z", keysz)
        keysa =[]
        keysb =[]
        
        keyssum1.append(keysy)
        #m = m1
        keyssum2.append(keysz)
        #m = m2
        #while True:
        #  pass
        
        keys =[]
       
        #points so far + how many points with the next step
        kAl= keysy[-1]
        kA = kAl[-1]
        kBl = keysz[-1]
        kB = kBl[-1]
        mcom1, done, pcom1 = AI_heuristics.commands[kA](m3)
        mcom2, done, pcom2 = AI_heuristics.commands[kB](m2)
        mcom12, done, pcom12 = AI_minimax.commands[kA](m3)
        mcom22, done, pcom22 = AI_minimax.commands[kB](m2)
        poicom1 = poicom1 +pcom1
        poicom2 = poicom2 +pcom2
        poicom12 = poicom12 +pcom12
        poicom22 = poicom22 +pcom22
        #print("PX", kA, pcom1, pcom12)
        keysy =[]
        keysz = []
        #print(keyssum)
    #while True:
    #    pass
    
    fkeys = []
    for r in keyssum1:
        for row in r:
            fkeys = fkeys + row
    keysA = fkeys
    fkeys2=[]
    for r in keyssum2:
        for row in r:
            fkeys2 = fkeys2 + row
    keysB = fkeys2
    
    print (kA, kB, poicom1, poicom2, poicom12, poicom22)
    if versum>=versum2*1 and poicom1 >= poicom2 and poicom12>=poicom22:
        keys = keysA
        #print("AAAAA")
        m = mcom1
    else:
        keys = keysB
        #print("BBBBB")
        m = mcom2

    print("*", keys)
    global over
    over = True
    if keys == keysor:
        if keys == keysA:
            keys = keysB
        else:
            keys = keysA
        print("Switch", keys)
        
    #if same keys serie and map ->random
    if keys == keysor and mold == m:
        keys = rand_keys()
        print("random", keys)
    return keys
def rand_keys():
    keys =[]
    for r in range(6):
        keys.append(tmp[random.randint(0,3)])
    global over
    over = False
    return keys

def read_keys(kes, mr):
    
    global inde2
    #print(inde2)
    if inde2 < 6:
        key = kes[inde2]
        inde2 = inde2 +1
    if inde2 >= 6:
            inde2 = 0
            global over
            over = False
    
    #print("!",key)
    
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
