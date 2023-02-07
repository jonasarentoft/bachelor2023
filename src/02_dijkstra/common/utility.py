import heapq as hq

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = set()

        self.distance = -1
        self.visited = False

    @staticmethod
    def add_edge(a, b, dist):
        a.edges.add((b, dist))
        
def dijkstra(start):
    h = []

    start.distance = 0

    hq.heappush(h, (start.distance, start))

    while len(h) > 0:

        cur = hq.heappop(h)

        # check if the nodes has been updated
        if cur[0] != cur[1].distance:
            continue

        for e in cur[1].edges:
            new_distance = cur[1].distance + e[1]

            if e[0].distance < 0 or new_distance < e[0].distance:
                e[0].distance = new_distance
                hq.heappush(h, (new_distance, e[0]))