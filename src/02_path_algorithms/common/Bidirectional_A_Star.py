import heapq as hq
from common.utility import GetPath
from common.DistanceFormula import DistanceFormula

def bidirectional_a_star(E, V, W, E_rev, V_rev, W_rev, lat, lon, startNode, endNode):
    forwardHeap = []
    backwardHeap = []
    hq.heappush(forwardHeap, (0, 0, startNode))
    hq.heappush(backwardHeap, (0, 0, endNode))

    intersection = False
    forwardDistances = {}
    forwardPrevious = {}
    forwardDistances[startNode] = 0
    latEndNode = lat[endNode]
    lonEndNode = lon[endNode]


    backwardDistances = {}
    backwardPrevious = {}
    backwardDistances[endNode] = 0
    latStarNode = lat[startNode]
    lonStartNode = lon[startNode]
    
    

    while forwardHeap or backwardHeap:
        if forwardHeap:
            curr_prio, currForwardDist, currForwardNode = hq.heappop(forwardHeap)
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
                    
                    
                    latToNode = lat[toNode]
                    lonToNode = lon[toNode]
                    
                    heuristic = DistanceFormula(latToNode, latEndNode, lonToNode, lonEndNode)
                    
                    
                    priority = new_dist + heuristic
                    
                    hq.heappush(forwardHeap, (priority, new_dist, toNode))
                      
        if backwardHeap:
            curr_prio, currBackwardDist, currBackwardNode = hq.heappop(backwardHeap)

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
                    
                    latToNode = lat[toNode]
                    lonToNode = lon[toNode]
                    
                    heuristic = DistanceFormula(latToNode, latStarNode, lonToNode, lonStartNode)
                    
                    
                    priority = new_dist + heuristic
                    
                    hq.heappush(backwardHeap, (priority, new_dist, toNode))

        if intersection:
            intersection = (backwardDistances.keys() & forwardDistances.keys())
            intersection = int(list(intersection)[0])
            path = GetPath(intersection, backwardPrevious)[::-1] + [intersection] + GetPath(intersection, forwardPrevious)
            return path, (forwardDistances | backwardDistances)