import heapq as hq

def initOrder(V, E, Weights, V_rev, E_rev, Weights_rev, shortCuts):
    heap = []

    for v in range(len(V) - 1):
        Ax = 0 # number of shortcuts added
        prio = {}
        prio[v] = 1
        U = [(u, weight) for u, weight in zip(E_rev[V_rev[v]:V_rev[v + 1]], Weights_rev[V_rev[v]:V_rev[v+1]])]
        W = [(w, weight) for w, weight in zip(E[V[v]:V[v + 1]], Weights[V[v]:V[v + 1]])]
        if U and W:
            for u, u_dist in U:
                key = lambda values: values[1]
                Pmax = u_dist + max(W, key = key)[1]
                distDict, prevs, _ = dijkstra(E, V, Weights, u, Pmax, prio, shortCuts)

                for w, w_dist in W:
                    if distDict.get(w) == None or distDict.get(w) > u_dist + w_dist:
                        Ax += 1
        hq.heappush(heap, (Ax - len(U), v))
    return heap


    

def lazyUpdate(prio, v, vShortCutDict, vShortCutDict_rev, V, E, Weights, V_rev, E_rev, Weights_rev,shortCuts):
    Ax = 0
    Wsc, Usc = [], []
    contractedNeighbs = V_rev[v+1] - V_rev[v]
    dijkstraResults = {}
    W = [(w, weight) for w, weight in zip(E[V[v]:V[v + 1]],Weights[V[v]:V[v + 1]]) if w not in prio.keys()]
    if vShortCutDict:
        Wsc = [(toNode, sc_weight) for toNode, (_, sc_weight) in vShortCutDict.items() if toNode not in prio.keys()]
    W = W + Wsc
    
    U = [(u, weight) for u, weight in zip(E_rev[V_rev[v]:V_rev[v + 1]], Weights_rev[V_rev[v]:V_rev[v+1]]) if u not in prio.keys()]
    contractedNeighbs -= len(U)
    if vShortCutDict_rev:
        Usc = [(fromNode, sc_weight) for fromNode, (_, sc_weight) in vShortCutDict_rev.items() if fromNode not in prio.keys()]
    U = U + Usc
    
    if U and W:
        for u, u_dist in U:
            key = lambda values: values[1]
            Pmax = u_dist + max(W, key = key)[1]
            distDict, prevs, _ = dijkstra(E, V, Weights, u, Pmax, prio, shortCuts)
            dijkstraResults[u] = distDict
            for w, w_dist in W:
                if distDict.get(w) == None or distDict.get(w) > u_dist + w_dist:
                    Ax += 1
    return Ax - len(U) + contractedNeighbs, U, W, dijkstraResults


def dijkstra(E, V, Weights, u, Pmax, prio, shortCuts):
    heap = []
    distances = {}
    previous = {}
    distances[u] = 0
    hq.heappush(heap, (0, u))
    stepCounter = 0
    while heap:

        curr_dist, curr_node = hq.heappop(heap)
        
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
                
        sc_dict = shortCuts.get(curr_node, {})
        
        for toNode, (_, dist) in sc_dict.items():

            if toNode in prio.keys():
                continue
                   
            distToNode = distances.get(toNode)
            new_dist = curr_dist + dist
            if distToNode == None or distToNode > new_dist:
                distances[toNode] = new_dist
                previous[toNode] = curr_node
                hq.heappush(heap, (new_dist, toNode))

        if not heap or heap[0][0] > Pmax:
            return distances, previous, stepCounter
    return distances, previous, stepCounter