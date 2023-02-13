import heapq as hq

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
        
        
    

        
def dijkstra(start):
    heap = []
    
    distances = {}
    previous = {}
    
    distances[start] = 0

    hq.heappush(heap, (distances[start], start))

    while heap:

        current = hq.heappop(heap)
        
        distance, node = current
        #print([e for e in current])
        

        # check if the nodes has been updated
        if distance != distances[node]:
            continue

        for e in node.edges:
            
            edgeNode, edgeDistance = e
            
            new_distance = distances[node] + edgeDistance

            if distances.get(edgeNode) is None or new_distance < distances[edgeNode]:
                
                # opdater dictionary
                distances[edgeNode] = new_distance
                previous[edgeNode.value] = node.value
                
                hq.heappush(heap, (new_distance, edgeNode))
                
    return distances, previous


def GetPath(target, previousDict):
    previous = previousDict.get(target)
    
    if previous is None:
        return []
    
    else:
        return [target] + GetPath(previous, previousDict)
    