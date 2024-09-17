import constants as c
import random
import AI_minimax
import AI_heuristics

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
def AI_play(m):
    #key=tmp[random.randint(0,3)]
    global maps
    maps = m
    #if stucked:
    key, mv = look(m)
    #mv, done, points = AI_heuristics.commands[key](m) 
    
    
    maximi = 0
    for k4 in AI_minimax.commands:
        pp, key2 = AI_heuristics.next_tile(maps, mv, k4)
        if pp >maximi:
            print("###")
            key = key2
            maximi = pp
            pp3, key3 = AI_heuristics.next_tile(maps, mv, key)
            if pp3>0:
                key = key3
    #end stuck
    print("¤", key)
    return key
def look(m):
    global over
    #print(over)
    if over == False:
        global keys1
        keys1 = make_keys(m)
    key, m = read_keys(keys1,m)
    
    return key, m

def make_keys(m):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
    #random initial directions
    #key=tmp[random.randint(0,3)]
    key = tmp[0]
    #k =tmp[random.randint(0,3)]
    k = tmp[1]
    map = m
    keys=[k]
    #print(keys)
    #key=tmp[random.randint(0,3)]
    for a in range(2):
        kmm = (AI_minimax.mima(m))
        k = AI_heuristics.AI_play(m)
        if k == kmm:
            key = k
        else:
            key = kmm
        keys.append(key)    
    print("*", keys)
    global over
    over = True
    return keys

def read_keys(kes, mr):
    
    global inde2
    print(inde2)
    if inde2<=2:
        key = kes[inde2]
        inde2 = inde2 +1
    if inde2 > 2:
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
