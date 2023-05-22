import heapq as hq
from common.DistanceFormula import DistanceFormula
import math
from common.Timer import *

@timer
def a_star(E, V, W, lat, lon, startNode, endNode):
    heap = []
    distances = {}
    previous = {}
    heuristics = {}
    distances[startNode] = 0
    hq.heappush(heap, (0,0, startNode))
    
    
    latEndNode = lat[endNode]
    lonEndNode = lon[endNode]
    while heap:
        curr_prio, curr_dist, curr_node = hq.heappop(heap)

        
        if curr_node == endNode:

            return distances, previous

 
        r = range(V[curr_node], V[curr_node+1])
     

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
                
                heuristics[toNode] = heuristic
                
                
                priority = new_dist + heuristic
                hq.heappush(heap, (priority, new_dist, toNode))
    return distances, previous