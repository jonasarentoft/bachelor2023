import heapq as hq
from common.DistanceFormula import DistanceFormula
import math

def a_star(E, V, W, lat, lon, startNode, endNode):
    heap = []
    distances = {}
    previous = {}
    distances[startNode] = 0
    hq.heappush(heap, (0, startNode))
    
    
    latEndNode = lat[endNode]
    lonEndNode = lon[endNode]
    while heap:
        curr_dist, curr_node = hq.heappop(heap)

        
        if curr_node == endNode:

            return distances, previous

        try:
            r = range(V[curr_node], V[curr_node+1])
        except:
            r = range(V[curr_node], len(E))

        for i in r:
            
            toNode = E[i]
            dist = W[i]
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or new_dist < distToNode:
        
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                
                latToNode = lat[toNode]
                lonToNode = lon[toNode]
                
                heuristic = DistanceFormula(latToNode, latEndNode, lonToNode, lonEndNode)
                
                
                priority = new_dist + heuristic
                hq.heappush(heap, (priority, toNode))
    return distances, previous