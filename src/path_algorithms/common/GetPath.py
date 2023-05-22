import heapq as hq
import sys

def GetPath(target, previousDict):
    previous = previousDict.get(target)
    
    previous = previousDict.get(target)
    path = [target]
    while previous:
        path = path + [previous]
        previous = previousDict.get(previous)
    return path
        



