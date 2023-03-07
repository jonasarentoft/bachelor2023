import heapq as hq
from common.utility import GetPath

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

    while forwardHeap or backwardHeap:
        if forwardHeap:
            currForwardDist, currForwardNode = hq.heappop(forwardHeap)
            try:
                r = range(V[currForwardNode], V[currForwardNode+1])
            except:
                r = range(V[currForwardNode], len(E))
                
            for i in r:
                toNode = E[i]
                if backwardDistances.get(toNode) != None:
                    intersection = True
                dist = W[i]
                
                distToNode = forwardDistances.get(toNode)
                new_dist = currForwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    forwardDistances[toNode] = new_dist
                    forwardPrevious[toNode] = currForwardNode
                    hq.heappush(forwardHeap, (new_dist, toNode))
                      
        if backwardHeap:
            currBackwardDist, currBackwardNode = hq.heappop(backwardHeap)

            try:
                r = range(V_rev[currBackwardNode], V_rev[currBackwardNode+1])
            except:
                r = range(V_rev[currBackwardNode], len(E_rev))


            for i in r:

                toNode = E_rev[i]
                if forwardDistances.get(toNode) != None:
                    intersection = True
                dist = W_rev[i]

                distToNode = backwardDistances.get(toNode)
                new_dist = currBackwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    backwardDistances[toNode] = new_dist
                    backwardPrevious[toNode] = currBackwardNode
                    hq.heappush(backwardHeap, (new_dist, toNode))

        if intersection:
            return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious
        