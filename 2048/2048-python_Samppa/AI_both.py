import constants as c
import random
import AI_minimax
import AI_heuristics


global inde1
inde1 = 0
keys = []
def AI_play(m):
    tmp = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
    key = c.KEY_LEFT 
    k = c.KEY_RIGHT
    map = m
    keys=[k]
    #key=tmp[random.randint(0,3)]
    maps = [m]
    global inde1
    if inde1>=0 and inde1<len(keys):
        
        keys, map = AI_minimax.play3(maps[inde1])
        k = AI_heuristics.AI_play(maps[inde1])
        #print("&&&", keys)
    #print(keys)
    if inde1>=0 and inde1<len(keys):
        key = keys[inde1]
        #print("!",key)
    if k == key:
        maps.append(map)
    inde1 = inde1 + 1
    #print(inde1, keys)
    if inde1 >= len(keys):
        inde1 = 0
    #print("*", key, inde1, len(keys))
    return key
