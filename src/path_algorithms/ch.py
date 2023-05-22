


 
import heapq as hq
import numpy as np


FILEPATH = 'data/processed/malta'

E = np.loadtxt(f'{FILEPATH}/E.txt', dtype=int)
V = np.loadtxt(f'{FILEPATH}/V.txt', dtype=int)
W = np.loadtxt(f'{FILEPATH}/W.txt', dtype=np.float32)

E_rev = np.loadtxt(f'{FILEPATH}/E_reversed.txt', dtype=int)
V_rev = np.loadtxt(f'{FILEPATH}/V_reversed.txt', dtype=int)
W_rev = np.loadtxt(f'{FILEPATH}/W_reversed.txt', dtype=np.float32)


names = {0: 'A',
         1: 'B',
         2: 'C', 
         3: 'D', 
         4: 'E', 
         5: 'F', 
         6: 'G', 
         7: 'H', 
         8: 'I', 
         9: 'J',
         10: 'K'}
def dijkstra(E, V, Weights, u, W, v, Pmax, prio, shortCuts, Vsc, Esc, Weights_shortcut):
    heap = []
    distances = {}
    previous = {}
    distances[u] = 0
    hq.heappush(heap, (0, u))

    while heap:
        curr_dist, curr_node = hq.heappop(heap)
        
        curr_node = int(curr_node)
        r = range(V[curr_node], V[curr_node+1])
        rshortcuts = range(Vsc[curr_node], Vsc[curr_node+1])
        
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
                
        
        for i in rshortcuts:
            
            toNode = Esc[i]
            if toNode in prio.keys():
                continue

            dist = Weights_shortcut[i]
            
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))
        
        if not heap or heap[0][0] > Pmax:
            return distances
    
        



# node  A, B, C, D, E, F, G, H, I, J, K
# node# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

# edges 3, 3, 4, 4, 3, 3, 3, 4, 4, 6, 3
# V = np.array([0, 3, 6, 10, 14, 17, 20, 23, 27, 31, 37, 40, 40])
# E = np.array([1, 2, 10,          
#     0, 2, 3,            
#     0, 1, 3, 9,         
#     1, 2, 4, 9,         
#     3, 5, 9,            
#     4, 6, 7,            
#     5, 7, 8,            
#     5, 6, 8, 9,         
#     6, 7, 9, 10,        
#     2, 3, 4, 7, 8, 10,  
#     0, 8, 9])
# Weights = np.array([3, 5, 3,
#     3, 3, 5,
#     5, 3, 2, 2,
#     5, 2, 7, 4,
#     7, 6, 3,
#     6, 4, 2,
#     4, 3, 5,
#     2, 3, 3, 2,
#     5, 3, 4, 6,
#     2, 4, 3, 2, 4, 3,
#     3, 6, 3])


distDict = {}
prio = {}
shortCuts = {}
shortcutKey = 0
# B E I K  B G C J H F A
# 1 4 8 10 1 6 2 9 7 5 0
antalKanter = np.array([V[i + 1] - V[i] + V_rev[i + 1] - V_rev[i] for i in range(len(V) - 1)])
ordering = np.argsort(antalKanter)

Weights = W

Vsc = np.array([0 for i in range(len(V))], dtype = int)
Esc = np.array([], dtype = int)
Weights_shortcut = np.array([], dtype = int)

Vsc_rev = np.array([0 for i in range(len(V))], dtype = int)
Esc_rev = np.array([], dtype = int)
Weights_shortcut_rev = np.array([], dtype = int)

#ordering = [1, 4, 8, 10, 3, 6, 2, 9, 7, 5, 0]
for i, node in enumerate(ordering):

    W = E[V[node]:V[node + 1]]
    
    # Add shortcut edges
    W = np.append(W, Esc[Vsc[node]:Vsc[node + 1]])
    W = [w for w in W if w not in prio.keys()]
    
    U = E[V[node]:V[node + 1]]
    U = np.hstack((U, Esc_rev[Vsc_rev[node]:Vsc_rev[node + 1]]))
    U = [u for u in U if u not in prio.keys()]
    
    prio[node] = i
    for u in U:
        # get distance dist(u, v)
        
        W_u = [Weights[toNode] for toNode in range(V[u], V[u + 1]) if E[toNode] == node]
        if not W_u:
            W_u = [Weights_shortcut[toNode] for toNode in range(Vsc[u], Vsc[u + 1]) if Esc[toNode] == node]
        # get distance dist(v, w) for all w in W
        Pw = [Weights[toNode] for toNode in range(V[node], V[node + 1]) for w in W if E[toNode] == w]
        Pw_sc = [Weights_shortcut[toNode] for toNode in range(Vsc[node], Vsc[node + 1]) for w in W if Esc[toNode] == w]
        Pw = np.append(Pw, Pw_sc)
    
        # get max of dist(u, v) + dist(v, w)
        Pmax = max(W_u, default = 0) + max(Pw, default = 0)
        
        # run dijkstra where Pmax is the search limit and prio 
        # contains contracted vertices as {vertice : contraction order}
        distDict = dijkstra(E, V, Weights, u, W, node, Pmax, prio, shortCuts, Vsc, Esc, Weights_shortcut)


        for j, w in enumerate(W):
            if distDict.get(w) == None or distDict.get(w) > Pmax:
                lastEdgeFromU = Vsc[u + 1]
                
                
                ## Normal Graph
                Esc = np.hstack((Esc[:lastEdgeFromU], w, Esc[lastEdgeFromU:]))
                Weights_shortcut = np.hstack((Weights_shortcut[:lastEdgeFromU],max(W_u, default = 0) + Pw[j], Weights_shortcut[lastEdgeFromU:]))
                index = u + 1
                Vsc = np.hstack((Vsc[:index], Vsc[index:] + 1))


                ## Reversed graph
                revEdge = Vsc_rev[w + 1]
                Esc_rev = np.hstack((Esc_rev[:revEdge], w, Esc_rev[revEdge:]))
                Weights_shortcut_rev = np.hstack((Weights_shortcut_rev[:revEdge],max(W_u, default = 0) + Pw[j], Weights_shortcut_rev[revEdge:]))
                index = w + 1
                Vsc_rev = np.hstack((Vsc_rev[:index], Vsc_rev[index:] + 1))

                shortCuts[w] = (u, w, W_u + Pw[j])
                shortcutKey += 1
                #print(f'Ny shortcut {u} --> {w}, v = {node}')
    if i % 10000 == 0:
        print(i)


Gdown = []
Gup = []

Vup  = np.zeros(len(V), dtype = int)
Eup  = np.array([], dtype =int)
Wup  = np.array([], dtype =int)

Vdown  = np.zeros(len(V), dtype = int)
Edown  = np.array([], dtype =int)
Wdown  = np.array([], dtype =int)

for v in range(len(V) - 1):
    v_prio = prio.get(v)
    for i in range(V[v], V[v+1]):
        w = E[i]
        w_prio = prio.get(w)
        #print(v_prio, w_prio, v)
        if v_prio < w_prio:
            Vup = np.hstack((Vup[:v+1], Vup[v+1:] + 1))
            Eup = np.append(Eup, w)
            Wup = np.append(Wup, Weights[i])
    for i in range(Vsc[v], Vsc[v+1]):
        w = Esc[i]
        w_prio = prio.get(w)

        if v_prio < w_prio:
            Vup = np.hstack((Vup[:v+1], Vup[v+1:] + 1))
            Eup = np.append(Eup, w)
            Wup = np.append(Wup, Weights_shortcut[i])

for v in range(len(V) - 1):
    v_prio = prio.get(v)
    for i in range(V_rev[v], V_rev[v+1]):
        w = E[i]
        w_prio = prio.get(w)

        if v_prio < w_prio:
            Vdown = np.hstack((Vdown[:v+1], Vdown[v+1:] + 1))
            Edown = np.append(Edown, w)
            Wdown = np.append(Wdown, Weights[i])

    for i in range(Vsc_rev[v], Vsc_rev[v+1]):
        w = Esc_rev[i]
        w_prio = prio.get(w)

        if v_prio < w_prio:
            Vdown = np.hstack((Vdown[:v+1], Vdown[v+1:] + 1))
            Edown = np.append(Edown, w)
            Wdown = np.append(Wdown, Weights_shortcut_rev[i])



 
print(f'{Vup}\n{Vdown}\n{Vsc+V}')


print(f'{Vup}\n{Eup}\n')


import heapq as hq

def bidirectional(E, V, W, E_rev, V_rev, W_rev, lat, lon, startNode, endNode):
    forwardHeap = []
    backwardHeap = []
    hq.heappush(forwardHeap, (0, startNode))
    hq.heappush(backwardHeap, (0, endNode))

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
            currForwardDist, currForwardNode = hq.heappop(forwardHeap)
            
            r = range(V[currForwardNode], V[currForwardNode+1])
            
                
            for i in r:
                toNode = E[i]
                dist = W[i]
                
                distToNode = forwardDistances.get(toNode)
                new_dist = currForwardDist + dist
                
        
                if distToNode == None or distToNode > new_dist:
                    forwardDistances[toNode] = new_dist
                    forwardPrevious[toNode] = currForwardNode
                    if backwardDistances.get(toNode) is not None and forwardDistances.get(toNode) is not None:
                        if backwardDistances.get(toNode) + forwardDistances.get(toNode) < u:
                            intersection = toNode
                            u = backwardDistances.get(toNode) + new_dist + forwardDistances[toNode]
                        
                    hq.heappush(forwardHeap, (new_dist, toNode))
            if forwardHeap and forwardHeap[0][0] > u:
                forwardHeap = []

        if backwardHeap:
            currBackwardDist, currBackwardNode = hq.heappop(backwardHeap)

            
            r = range(V_rev[currBackwardNode], V_rev[currBackwardNode+1])
            


            for i in r:

                
                toNode = E_rev[i]
                
                dist = W_rev[i]

                distToNode = backwardDistances.get(toNode)
                new_dist = currBackwardDist + dist
                if distToNode == None or distToNode > new_dist:
                    backwardDistances[toNode] = new_dist
                    backwardPrevious[toNode] = currBackwardNode
                    if backwardDistances.get(toNode) is not None and forwardDistances.get(toNode) is not None:
                        if backwardDistances.get(toNode) + forwardDistances.get(toNode) < u:
                            intersection = toNode
                            u = backwardDistances.get(toNode) + forwardDistances[toNode]
                    hq.heappush(backwardHeap, (new_dist, toNode))

       
            if backwardHeap and backwardHeap[0][0] > u:
                backwardHeap = []
    return forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection


res = bidirectional(Eup, Vup, Wup, Edown, Vdown, Wdown, 0, 0, 0, 6)

print(res[0], res[1])

# NN = ['A','B','C','D','E','F','G','H','I','J', 'K']
# for i in range(len(Vdown)- 1):
#     r = range(Vdown[i], Vdown[i+1])
#     for j in r:
#         print(f'Path from {NN[i]} to {NN[Edown[j]]}')








