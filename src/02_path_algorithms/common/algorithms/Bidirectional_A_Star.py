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
    latStartNode = lat[startNode]
    lonStartNode = lon[startNode]

    backwardDistances = {}
    backwardPrevious = {}
    backwardDistances[endNode] = 0
    
    u = 100000

    while forwardHeap or backwardHeap:
        if forwardHeap:
            curr_prio, currForwardDist, currForwardNode = hq.heappop(forwardHeap)
            
            r = range(V[currForwardNode], V[currForwardNode+1])
            

            for i in r:
                toNode = E[i]
                
                dist = W[i]
                
                distToNode = forwardDistances.get(toNode)
                new_dist = currForwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    
                    latToNode = lat[toNode]
                    lonToNode = lon[toNode]
                    heuristic = DistanceFormula(latToNode, latEndNode, lonToNode, lonEndNode)
                    
                    forwardDistances[toNode] = new_dist
                    forwardPrevious[toNode] = currForwardNode
                    
                    priority = new_dist + heuristic
                    if backwardDistances.get(toNode) and backwardDistances.get(toNode) + new_dist < u:
                        intersection = toNode
                        u = backwardDistances.get(toNode) + new_dist
                    
                    
                    hq.heappush(forwardHeap, (priority, new_dist, toNode))
        if backwardHeap:
            curr_prio, currBackwardDist, currBackwardNode = hq.heappop(backwardHeap)

            
            r = range(V_rev[currBackwardNode], V_rev[currBackwardNode+1])
            

            for i in r:
                toNode = E_rev[i]
                
                dist = W_rev[i]

                distToNode = backwardDistances.get(toNode)
                new_dist = currBackwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    
                    latToNode = lat[toNode]
                    lonToNode = lon[toNode]
                    heuristic = DistanceFormula(latToNode, latStartNode, lonToNode, lonStartNode)
                    
                    priority = new_dist + heuristic

                    if forwardDistances.get(toNode) and forwardDistances.get(toNode) + new_dist < u:
                        intersection = toNode
                        u = forwardDistances.get(toNode) + new_dist

                    backwardDistances[toNode] = new_dist
                    backwardPrevious[toNode] = currBackwardNode

                    hq.heappush(backwardHeap, (priority, new_dist, toNode))
                    
        if not forwardHeap or not backwardHeap:
            return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, None

        if u <= max(forwardHeap[0][0], backwardHeap[0][0]):
            return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection