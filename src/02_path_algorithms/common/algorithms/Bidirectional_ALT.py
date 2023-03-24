import heapq as hq
from common.utility import GetPath
from common.DistanceFormula import DistanceFormula

def bidirectional_alt(E, V, W, E_rev, V_rev, W_rev, startNode, endNode, distancesToLandmarks, distancesFromLandmarks):
    forwardHeap = []
    backwardHeap = []
    hq.heappush(forwardHeap, (0, 0, startNode))
    hq.heappush(backwardHeap, (0, 0, endNode))

    intersection = False
    forwardDistances = {}
    forwardPrevious = {}

    forwardDistances[startNode] = 0

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
                    
                    pi_plus = max([distancesToLandmarks[landmark][toNode] - distancesToLandmarks[landmark][endNode] for landmark in distancesToLandmarks])
                    pi_minus = max([distancesFromLandmarks[landmark][endNode] - distancesFromLandmarks[landmark][toNode] for landmark in distancesFromLandmarks])
                    #pi_plus = np.nan_to_num(pi_plus, 0)
                    #pi_minus = np.nan_to_num(pi_minus, 0)
                    
                    heuristic = max(pi_plus,pi_minus)
                    
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
                    
                    pi_plus = max([distancesFromLandmarks[landmark][toNode] - distancesFromLandmarks[landmark][startNode] for landmark in distancesToLandmarks])
                    pi_minus = max([distancesToLandmarks[landmark][startNode] - distancesToLandmarks[landmark][toNode] for landmark in distancesFromLandmarks])
                    #pi_plus = np.nan_to_num(pi_plus, 0)
                    #pi_minus = np.nan_to_num(pi_minus, 0)
                    
                    heuristic = max(pi_plus,pi_minus)
                    
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