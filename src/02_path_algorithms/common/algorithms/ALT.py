import heapq as hq
import math
import numpy as np

def alt(E, V, W, lat, lon, startNode, endNode, distancesToLandmarks, distancesFromLandmarks):
    heap = []
    distances = {}
    previous = {}
    distances[startNode] = 0
    hq.heappush(heap, (0,0, startNode))
    

    while heap:
        _, curr_dist, curr_node = hq.heappop(heap)

        
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
                
                pi_plus = max([distancesToLandmarks[landmark][toNode] - distancesToLandmarks[landmark][endNode] for landmark in distancesToLandmarks])
                pi_minus = max([distancesFromLandmarks[landmark][endNode] - distancesFromLandmarks[landmark][toNode] for landmark in distancesFromLandmarks])
                #pi_plus = np.nan_to_num(pi_plus, 0)
                #pi_minus = np.nan_to_num(pi_minus, 0)
                
                heuristic = max(pi_plus,pi_minus)
                
                priority = new_dist + heuristic
                hq.heappush(heap, (priority, new_dist, toNode))
    return distances, previous