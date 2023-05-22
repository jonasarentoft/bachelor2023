import heapq as hq

def dijkstra(E, V, Weights, u, W, v, Pmax, prio, shortCuts):
    heap = []
    distances = {}
    previous = {}
    distances[u] = 0
    hq.heappush(heap, (0, u))

    while heap:
        curr_dist, curr_node = hq.heappop(heap)
        if curr_node in prio.keys():
            continue

        r = range(V[curr_node], V[curr_node+1])
        
        for i in r:
            
            toNode = E[i]
            if toNode in prio.keys():
                continue
            dist = Weights[i]
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))
        
        for fromNode, (toNode, dist) in shortCuts.items():
            if fromNode == curr_node:
                distToNode = distances.get(toNode)
                new_dist = curr_dist + dist
                if distToNode == None or distToNode > new_dist:
                    distances[toNode] = new_dist
                    previous[toNode] = curr_node
                    hq.heappush(heap, (new_dist, toNode))


        if not heap or heap[0][0] >= Pmax:
            return distances
    return distances

import numpy as np
# node  A, B, C, D, E, F, G, H, I, J, K
# node# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

# edges 3, 3, 4, 4, 3, 3, 3, 4, 4, 6, 3
V = np.array([0, 3, 6, 10, 14, 17, 20, 23, 27, 31, 37, 40, 40])
E = np.array([1, 2, 10,          
    0, 2, 3,            
    0, 1, 3, 9,         
    1, 2, 4, 9,         
    3, 5, 9,            
    4, 6, 7,            
    5, 7, 8,            
    5, 6, 8, 9,         
    6, 7, 9, 10,        
    2, 3, 4, 7, 8, 10,  
    0, 8, 9])
Weights = np.array([3, 5, 3,
    3, 3, 5,
    5, 3, 2, 2,
    5, 2, 7, 4,
    7, 6, 3,
    6, 4, 2,
    4, 3, 5,
    2, 3, 3, 2,
    5, 3, 4, 6,
    2, 4, 3, 2, 4, 3,
    3, 6, 3])


distDict = {}
prio = {}
shortCuts = {}
shortcutKey = 0
# B E I K  B G C J H F A
# 1 4 8 10 1 6 2 9 7 5 0
ordering = np.array([1, 4, 8, 10, 3, 6, 2, 9, 7, 5, 0])

for i, node in enumerate(ordering):

    W_raw = E[V[node]:V[node + 1]]
    W = [w for w in W_raw if w not in prio.keys()]
    W += [toNode for fromNode, (toNode, weight) in shortCuts.items() if fromNode == node]
    
    U_raw = E[V[node]:V[node + 1]]
    U = [u for u in U_raw if u not in prio.keys()]
    U += [fromNode for fromNode, (toNode, weight) in shortCuts.items() if toNode == node]
    
    prio[node] = i

    for k, u in enumerate(U):
        W_u = []
        
        # get distance dist(u, v)
        
        W_u = [weight for fromNode, (toNode, weight) in shortCuts.items() if toNode == node]    
        
        
        if not W_u:
            W_u = [Weights[toNode] for toNode in range(V[u], V[u + 1]) if E[toNode] == node][0]
        #W_u += [weight for fromNode, (toNode, weight) in shortCuts.items() if toNode == node]
        
        
        # get distance dist(v, w) for all w in W
        neighbourRange = range(V[node], V[node + 1])
        Pw = [Weights[toNode] for toNode in neighbourRange for w in W if E[toNode] == w]
        Pw += [weight for fromNode, (toNode, weight) in shortCuts.items() if fromNode == node]
        
        # get max of dist(u, v) + dist(v, w)
        Pmax = W_u + max(Pw)
        
        # run dijkstra where Pmax is the search limit and prio 
        # contains contracted vertices as {vertice : contraction order}
        distDict = dijkstra(E, V, Weights, u, W, node, Pmax, prio, shortCuts)

    
        for j, w in enumerate(W):
            
            if distDict.get(w, 0) > W_u + Pw[j]:
                
                
                
                try:
                    shortCuts[u].append((w, W_u + Pw[j]))
                    
                except:
                    shortCuts[u] = [(w, W_u + Pw[j])]
                    
                shortcutKey += 1
                print(f'Ny shortcut {u} --> {w}, v = {node}')
                
    
                
                