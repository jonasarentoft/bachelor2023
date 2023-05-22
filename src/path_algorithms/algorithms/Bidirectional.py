import heapq as hq
from common.GetPath import GetPath
import time
from common.Timer import *

@timer
def bidirectional(E, V, W, E_rev, V_rev, W_rev, lat, lon, startNode, endNode):
    forwardHeap = []
    backwardHeap = []
    hq.heappush(forwardHeap, (0, startNode))
    hq.heappush(backwardHeap, (0, endNode))

    intersection = False
    forwardDistances = {}
    forwardPrevious = {}
    forwardDistances[startNode] = 0


    backwardDistances = {}
    backwardPrevious = {}
    backwardDistances[endNode] = 0
    u = 100000
    while forwardHeap and backwardHeap:
        #if forwardHeap:
        currForwardDist, currForwardNode = hq.heappop(forwardHeap)
        
        r = range(V[currForwardNode], V[currForwardNode+1])
        
            
        for i in r:
            toNode = E[i]
            dist = W[i]
            
            distToNode = forwardDistances.get(toNode)
            new_dist = currForwardDist + dist
            
    
            if distToNode == None or distToNode > new_dist:
                if backwardDistances.get(toNode) and backwardDistances.get(toNode) + new_dist < u:
                    intersection = toNode
                    u = backwardDistances.get(toNode) + new_dist
                forwardDistances[toNode] = new_dist
                forwardPrevious[toNode] = currForwardNode
                hq.heappush(forwardHeap, (new_dist, toNode))

        #if backwardHeap:
        currBackwardDist, currBackwardNode = hq.heappop(backwardHeap)

        
        r = range(V_rev[currBackwardNode], V_rev[currBackwardNode+1])
        
        for i in r:

            toNode = E_rev[i]
            
            dist = W_rev[i]

            distToNode = backwardDistances.get(toNode)
            new_dist = currBackwardDist + dist
            if distToNode == None or distToNode > new_dist:
                if forwardDistances.get(toNode) and forwardDistances.get(toNode) + new_dist < u:
                    intersection = toNode
                    u = forwardDistances.get(toNode) + new_dist
                backwardDistances[toNode] = new_dist
                backwardPrevious[toNode] = currBackwardNode
                hq.heappush(backwardHeap, (new_dist, toNode))

        
        if u < forwardHeap[0][0] + backwardHeap[0][0]:
            return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection
        
    return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, None
        
    