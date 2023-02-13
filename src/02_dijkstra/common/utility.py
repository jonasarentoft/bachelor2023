import heapq as hq

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = set()

    @staticmethod
    def add_edge(a, b, dist):
        a.edges.add((b, dist))

        
def dijkstra(start):
    heap = []
    
    distances = {}
    
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
                hq.heappush(heap, (new_distance, edgeNode))
                
    return distances