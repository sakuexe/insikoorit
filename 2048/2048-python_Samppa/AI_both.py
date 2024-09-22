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
            #key, mv = look(mv)
            mv, done, points = AI_heuristics.commands[key](mv) 
            zer = AI_heuristics.zero(mv)
            if zer == 0 and maps == mv:
                empty = False
            else:
                empty = True
    #print("Z", zer)
    #print("¤", key)     
    
    return key
def look(m):
    #print(over)
    global keys1
    global keyolds
    keyolds  = keys1
    if over == False:    
        keys1 = make_keys(m)
        global inde2
        inde2 = 0
    mva = m
    key, m = read_keys(keys1,m)
    #print("#", key)
    #if keys1 == keyolds and m == mva:
    #    global GameOver
    #    GameOver =  True 
    return key, m


def make_keys(m):
    global keyolds
    keysor = keyolds
    keys =[]
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
    #random initial directions
    #key=tmp[random.randint(0,3)]
    key = tmp[0]
    #k =tmp[random.randint(0,3)]
    k = tmp[1]
    kmc = c.KEY_RIGHT
    kmm = tmp[2]
    map = m
    poicom1=0
    poicom2 = 0
    poicom3 =0
    poicom12 = 0
    poicom22 = 0
    poicom32 = 0
    #print(keys)
    #key=tmp[random.randint(0,3)]
    
        #kmm = (AI_minimax.mima(m))
        #k = AI_heuristics.AI_play(m)
    keyssum1 = []
    keyssum2 = []
    keyssum3 = []
    sumheura=0
    summ = 0
    m1 = m
    m2 = m
    m3 = m
    m4 = m
    keysa = []
    keysa2 =[]
    keysb = []
    keysc = []
    a = 0
    pka = 0
    keysy = []
    keysz = []
    keysw = []
    versum = 0
    versum2 =0 
    versum3=0
    mold2 = m
    
    first = True
    N = 0
    a = 0
    for l in range (3):
       
        for z in range(3):
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
        for v in range(3):
            N = tmp.index(kmm)
            NC = N + 1
            if kmm == k and l == 0:
                N = N + 1
                if N == 4:
                    N = 0
                kmm = tmp[N]
                NC = NC +1
                if NC >=4:
                    NC = 0
                kmc = tmp[NC]
            km= AI_heuristics.AI_play(m2)
            m2, done, pointsb = AI_heuristics.commands[km](m2)
            versum2 = versum2+pointsb
            k= AI_minimax.AI_play(m)
            m, done, pointsa2 = AI_heuristics.commands[k](m)
            keysa2.append(k)

            #AI_heuristics.AI_play(m2)
               #!!!! strategies have different first step
            #print("1", k, kmm, N)
            #Strategy C purely minimax
            kmc = AI_minimax.AI_play(m4)
            m4, done, pointsc = AI_minimax.commands[kmc](m4)
            kmc = (AI_minimax.mima(m4))
            
            #print("2", k, kmm, kmc, N, NC)

            keysb.append(kmm)
            keysc.append(kmc)
            summ=summ+pointsa2
            #versum = versum + sumheura
            versum3 = versum3 + pointsc
            #print("S", summ)
        #heuristcs 2 times more weight
        if sumheura> summ:
            keysy.append(keysa)
            mold = m1 
            #print("heu")
            versum = versum + sumheura
            #versum2 = versum2 + sumheura
            #versum3 = versum3 +sumheura
            #print(keysy)
        else:
            keysy.append(keysa2)
            mold =m1
            #print("minimax")  
            versum = versum + summ
            #versum2 = versum2 + sumheura
            #versum3 = versum3 + summ
        keysz.append(keysb)
        keysw.append(keysc)
        #print("Y", keysy)
        #print("Z", keysz)
        #print("W", keysw)
        
        keysa =[]
        keysb =[]
        keysc =[]
        keyssum1.append(keysy)
        #m = m1
        keyssum2.append(keysz)

        #m = m2
        keyssum3.append(keysw)
        #while True:
        #  pass
        
        keys =[]
       
        #points so far + how many points with the next step
        kAl= keysy[-1]
        kA = kAl[-1]
        kBl = keysz[-1]
        kB = kBl[-1]
        kCl = keysw[-1]
        kC = kCl[-1]
        
        mcom1, done, pcom1 = AI_heuristics.commands[kA](m1)
        mcom2, done, pcom2 = AI_heuristics.commands[kB](m2)
        mcom3, done, pcom3 = AI_heuristics.commands[kC](m4)
        mcom12, done, pcom12 = AI_minimax.commands[kA](m1)
        mcom22, done, pcom22 = AI_minimax.commands[kB](m2)
        mcom23, done, pcom32 = AI_minimax.commands[kC](m4)
        poicom1 = poicom1 +pcom1
        poicom2 = poicom2 +pcom2
        poicom3 = poicom3  + pcom3
        poicom12 = poicom12 +pcom12
        poicom22 = poicom22 +pcom22
        poicom32 = poicom32 + pcom32
        
        #print("PX", kA, pcom1, pcom12)
        keysy =[]
        keysz = []
        keysw =[]
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
    fkeys3 =[]
    for r in keyssum3:
        for row in r:
            fkeys3 = fkeys3 + row
    keysC = fkeys3
    #weigth for the best strategy A
    versum = versum*2
    #weight for the solely heuristic B Strategy 
    versum2=versum2*4
    #weight for the solely minimax C Strategy
    versum3=versum3*4
    #print(versum, versum2, versum3)
    print ("@", versum, versum2, versum3)
   #print (kA, kB, poicom1, poicom2, poicom12, poicom22)
    if versum>versum2 and versum>versum3: 
        #and poicom1 >= poicom2 and poicom12>=poicom22:
        keys = keysA
        print("AAAAA")
        m = mcom1
    elif versum2>=versum3 :
        #and poicom2 >= poicom3 and poicom22>=poicom32:
        keys = keysB
        print("BBBBB")
        m = mcom2
    else:
        keys = keysC
        print("CCCCC")
        m = mcom23
    #while True:
    #    pass
    
    global over
    over = True
    while keys == keysor:
        if keys == keysA:
            keys = keysB
            m = m2
            
            if keys[0] == keysA[0]:
                keys = keysC
                iid = tmp.index(keys[0])+1
                if iid >=4:
                    iid = 0
                keys[0]=tmp[iid]
                #AI_heuristics.next_tile(m, m3, keysA[0])
                m = m3
        
        elif keys == keysB:
            keys = keysC
            m = m4
            
            if keys[0]==keysB[0]:
                iid = tmp.index(keys[0])+1
                if iid >=4:
                    iid = 0
                keys[0]=tmp[iid]
                #pp, keys[0]= AI_heuristics.next_tile(m, m3, keysB[0])
                
        elif keys == keysC:
            keys = keysB
            m = m2
            
            if keys[0]==keysC[0]:
                iid = tmp.index(keys[0])+1
                if iid >=4:
                    iid = 0
                keys[0]=tmp[iid]
                #pp, keys[0]= AI_heuristics.next_tile(m, m3, keysC[0])
        over = False
        global inde2
        inde2 = 0
        print("*", keysor)
        print("Switch", keys)
        
    #if same keys serie and map ->random
    if keys == keysor and mold == m:
        keys = rand_keys()
        #print("random", keys)
    keysor = keys
    return keys
def rand_keys():
    keys =[]
    for r in range(9):
        keys.append(tmp[random.randint(0,3)])
    global over
    over = False
    return keys

def read_keys(kes, mr):
    
    global inde2
    #print(inde2)
    if inde2 < 9:
        key = kes[inde2]
        inde2 = inde2 +1
    if inde2 >= 9:
            indez = 0
            global over
            over = False
    
    #print("!",key)
    
    #print("*", key, inde1, len(keys))
    keyser5, mv3 = AI_minimax.play3(mr)
    return key, mv3
