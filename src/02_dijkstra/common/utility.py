import heapq as hq
import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = set()
        self.tmp = 0

    @staticmethod
    def add_edge(a, b, dist):
        a.edges.add((b, dist))

    def __eq__(self, other):
        return (self.tmp == other.tmp)

    def __ne__(self, other):
        return (self.tmp != other.tmp)

    def __lt__(self, other):
        return (self.tmp < other.tmp)

    def __gt__(self, other):
        return (self.tmp > other.tmp)

    def __le__(self, other):
        return (self.tmp < other.tmp) or (self.tmp == other.tmp)

    def __ge__(self, other):
        return (self.tmp > other.tmp) or (self.tmp == other.tmp)
    
    def __hash__(self):
        return hash(repr(self))
        
        
    

        
def dijkstra(E,V,W, startnode):
    heap = []
    distances = {}
    previous = {}
    distances[startnode] = 0
    hq.heappush(heap, (0, startnode))
    

    
    for i in range(len(V)):
        distances[i] = 100000

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


def GetPath(target, previousDict):
    
    previous = previousDict.get(target)
    
    if previous is None:
        return []
    
    else:
        return [target] + GetPath(previous, previousDict)
    