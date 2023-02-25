import heapq as hq
import sys

def GetPath(target, previousDict):
    previous = previousDict.get(target)
    
    previous = previousDict.get(target)
    path = []
    while previous:
        path = path + [previous]
        previous = previousDict.get(previous)
    return path
        
def dijkstra(E,V,W, startnode):
    heap = []
    distances = {}
    previous = {}
    distances[startnode] = 0
    hq.heappush(heap, (0, startnode))
    

    
    

    while heap:
        curr_dist, curr_node = hq.heappop(heap)
        
        try:
            r = range(V[curr_node], V[curr_node+1])
        except:
            r = range(V[curr_node], len(E))


        for i in r:
            
            toNode = E[i]
            dist = W[i]
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))
    
    return distances, previous



    