import heapq as hq
import numpy as np
from common.Timer import *


def bidirectional_CH(E, V, W, E_rev, V_rev, W_rev, shortCuts, shortCuts_rev, startNode, endNode, prio):
    forwardHeap = []
    backwardHeap = []
    hq.heappush(forwardHeap, (0, startNode))
    hq.heappush(backwardHeap, (0, endNode))

    intersection = None
    forwardDistances = {}
    forwardPrevious = {}
    forwardDistances[startNode] = 0


    backwardDistances = {}
    backwardPrevious = {}
    backwardDistances[endNode] = 0
    u = np.inf

    while forwardHeap or backwardHeap:
        if forwardHeap:
            currForwardDist, currForwardNode = hq.heappop(forwardHeap)
            
            r = range(V[currForwardNode], V[currForwardNode+1])
            
            forwardShortcuts = shortCuts.get(currForwardNode)

            for i in r:
                
                toNode = E[i]
                if  prio.get(currForwardNode) > prio.get(toNode):
                    continue
                
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

            for toNode, (_, dist) in forwardShortcuts.items():
                if  prio.get(currForwardNode) > prio.get(toNode):
                    continue
                
                distToNode = forwardDistances.get(toNode)
                new_dist = currForwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    if backwardDistances.get(toNode) and backwardDistances.get(toNode) + new_dist < u:
                        intersection = toNode
                        u = backwardDistances.get(toNode) + new_dist
                    forwardDistances[toNode] = new_dist
                    forwardPrevious[toNode] = currForwardNode
                    hq.heappush(forwardHeap, (new_dist, toNode))

        if backwardHeap:
            currBackwardDist, currBackwardNode = hq.heappop(backwardHeap)

            r = range(V_rev[currBackwardNode], V_rev[currBackwardNode+1])
            
            backwardShortcuts = shortCuts_rev.get(currBackwardNode)

            for i in r:

                toNode = E_rev[i]
                if  prio.get(currBackwardNode) > prio.get(toNode):
                    continue
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

            for toNode, (_, dist) in backwardShortcuts.items():
                if  prio.get(currBackwardNode) > prio.get(toNode):
                    continue
                
                distToNode = backwardDistances.get(toNode)
                new_dist = currBackwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    if forwardDistances.get(toNode) and forwardDistances.get(toNode) + new_dist < u:
                        intersection = toNode
                        u = forwardDistances.get(toNode) + new_dist
                    backwardDistances[toNode] = new_dist
                    backwardPrevious[toNode] = currBackwardNode
                    hq.heappush(backwardHeap, (new_dist, toNode))

    if forwardHeap and backwardHeap and u < forwardHeap[0][0] + backwardHeap[0][0]:
            return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection
        
    return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection
