import heapq as hq

def dijkstraCH(E, V, W, shortCutsDict, startNode, endNode, prio):
    heap = []
    distances = {}
    previous = {}
    distances[startNode] = 0
    hq.heappush(heap, (0, startNode))
    

    while heap:
        curr_dist, curr_node = hq.heappop(heap)
        
        r = range(V[curr_node], V[curr_node+1])
        
        curr_sc_dict = shortCutsDict.get(curr_node)

        for i in r:
            
            toNode = E[i]
            if  prio.get(curr_node) > prio.get(toNode):
                continue
            
            dist = W[i]
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))

        for toNode, (_, dist) in curr_sc_dict.items():
            if  prio.get(curr_node) > prio.get(toNode):
                continue
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))

    return distances, previous
