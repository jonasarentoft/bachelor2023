import random

import heapq as hq
import numpy as np

FILEPATH = "data/processed/isle"
file = f'{FILEPATH}/nodesAndPositions.txt'
lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)

E = np.loadtxt(f'{FILEPATH}/E.txt', dtype=int)
V = np.loadtxt(f'{FILEPATH}/V.txt', dtype=int)
Weights = np.loadtxt(f'{FILEPATH}/W.txt', dtype=np.float32)

E_rev = np.loadtxt(f'{FILEPATH}/E_reversed.txt', dtype=int)
V_rev = np.loadtxt(f'{FILEPATH}/V_reversed.txt', dtype=int)
Weights_rev = np.loadtxt(f'{FILEPATH}/W_reversed.txt', dtype=np.float32)


import heapq as hq

def dijkstra(E, V, Weights, Esc, Vsc, Weights_shortcut, u, Pmax, prio):
    heap = []
    distances = {}
    previous = {}
    distances[u] = 0
    hq.heappush(heap, (0, u))
    stepCounter = 0
    while heap:
        #stepCounter += 1
        curr_dist, curr_node = hq.heappop(heap)
        
        r = range(V[curr_node], V[curr_node+1])
        r_sc = range(Vsc[curr_node], Vsc[curr_node+1])
        
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
                
        
        for j in r_sc:
            
            toNode = Esc[j]
            if toNode in prio.keys():
                continue

            dist = Weights_shortcut[j]
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))
        if stepCounter >= 10:
           return distances, previous, stepCounter
        if not heap or heap[0][0] > Pmax:
            return distances, previous, stepCounter
    return distances, previous, stepCounter
        
        
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################        


distDict = {}
prio = {}
shortCuts = {}
shortCuts_rev = {}
shortcutKey = 0
# B E I K  B G C J H F A
# 1 4 8 10 1 6 2 9 7 5 0
antalKanter = np.array([V_rev[i + 1] - V_rev[i] for i in range(len(V) - 1)])
ordering = np.argsort(antalKanter)
#ordering = [1, 4, 8, 10, 3, 6, 2, 9, 7, 5, 0]

Vsc = np.array([0 for i in range(len(V))], dtype = int)
Esc = np.array([], dtype = int)
Weights_shortcut = np.array([], dtype = np.float32)

Vsc_rev = np.array([0 for i in range(len(V))], dtype = int)
Esc_rev = np.array([], dtype = int)
Weights_shortcut_rev = np.array([], dtype = np.float32)

for i, v in enumerate(ordering):
    
    # Get all nodes that can be reached from v, - (v, u)
    W = E[V[v]:V[v + 1]]
    W = np.append(W, Esc[Vsc[v]:Vsc[v + 1]])
    W = [w for w in W if w not in prio.keys()]
    
    # Get all nodes, W, that have an edge to v - (u, v)
    U = E_rev[V_rev[v]:V_rev[v + 1]]
    U = np.append(U, Esc_rev[Vsc_rev[v]:Vsc_rev[v + 1]])
    U = [u for u in U if u not in prio.keys()]
    
    prio[v] = i

    for u in U:
        # get distance dist(u, v)
        W_u = [Weights[edge] for edge in range(V[u], V[u + 1]) if E[edge] == v]
        # if edge (u, v) is not in E, then the edge is a shortcut
        if not W_u:
            W_u = [Weights_shortcut[edge] for edge in range(Vsc[u], Vsc[u + 1]) if Esc[edge] == v]
        W_u = max(W_u, default = 0)
            
        # get distance dist(v, w) for all w in W
        Pw = [Weights[edge] for w in W for edge in range(V[v], V[v + 1]) if E[edge] == w]
        Pw_sc = [Weights_shortcut[edge] for w in W for edge in range(Vsc[v], Vsc[v + 1]) if Esc[edge] == w]
        Pw = np.append(Pw, Pw_sc)

        # get max of dist(u, v) + dist(v, w) for all w in W
        Pmax = W_u + max(Pw, default = 0)
        
        # run dijkstra where Pmax is the search limit and prio 
        # contains contracted vertices as {vertice : contraction order}
        distDict, prevs, _ = dijkstra(E, V, Weights, Esc, Vsc, Weights_shortcut, u, Pmax, prio)


        for j, w in enumerate(W):
            if distDict.get(w) == None or distDict.get(w) > W_u + Pw[j]:
                index = u + 1
                lastEdgeFromU = Vsc[index]
                Esc = np.hstack((Esc[:lastEdgeFromU], w, Esc[lastEdgeFromU:]))
                Weights_shortcut = np.hstack((Weights_shortcut[:lastEdgeFromU], W_u + Pw[j], Weights_shortcut[lastEdgeFromU:]))
                Vsc = np.hstack((Vsc[:index], Vsc[index:] + 1))

                index = w + 1
                revEdge = Vsc_rev[index]
                Esc_rev = np.hstack((Esc_rev[:revEdge], u, Esc_rev[revEdge:]))
                Weights_shortcut_rev = np.hstack((Weights_shortcut_rev[:revEdge], W_u + Pw[j], Weights_shortcut_rev[revEdge:]))
                Vsc_rev = np.hstack((Vsc_rev[:index], Vsc_rev[index:] + 1))

                shortCuts[u, w] = (v, W_u + Pw[j])
                shortCuts_rev[w, u] = (v, W_u + Pw[j])
                # print(f'Ny shortcut {u} --> {w}, v = {node}')
    if i % 10000 == 0:
        print(i, len(shortCuts))