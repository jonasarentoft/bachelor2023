import heapq as hq
import math
import numpy as np

def alt(E, V, W, lat, lon, startNode, endNode, distancesToLandmarks, distancesFromLandmarks):
    heap = []
    distances = {}
    previous = {}
    distances[startNode] = 0
    hq.heappush(heap, (0,0, startNode))
    
    pathExists = any([not np.isnan(distancesToLandmarks[landmark][startNode]) and not np.isnan(distancesFromLandmarks[landmark][endNode]) for landmark in distancesFromLandmarks])
    print(pathExists)
    
    
    if not pathExists:
        return distances, previous
    
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
                
                
                #pi_plus = max([distancesToLandmarks[landmark][toNode] - distancesToLandmarks[landmark][endNode] for landmark in distancesToLandmarks])
                #pi_minus = max([distancesFromLandmarks[landmark][endNode] - distancesFromLandmarks[landmark][toNode] for landmark in distancesFromLandmarks])
                
                pi_plus = max(distancesToLandmarks[0][toNode] - distancesToLandmarks[0][endNode])
                pi_minus = max(distancesFromLandmarks[0][endNode] - distancesFromLandmarks[0][toNode])
                
                heuristic = max(pi_plus,pi_minus)
                
                priority = new_dist + heuristic
                hq.heappush(heap, (priority, new_dist, toNode))
    return distances, previous