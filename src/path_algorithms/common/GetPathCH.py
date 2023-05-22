
def getIntersectNodeCH(distsUp, prevsUp, distsDown, prevsDown, shortCuts):
    dists = {}
    for key, d1 in distsUp.items():
        d2 = distsDown.get(key)
        if d2 != None :
            dists[key] = d1 + d2
    intersectNode = min(dists, key = dists.get)

    return intersectNode

def unpack_shortcut(parent, current, shortCuts):
    sc_dict = shortCuts.get(parent)
    contractedNode, weight = sc_dict.get(current, (None, None))
    
    if contractedNode == None:
        return []

    left = unpack_shortcut(parent, contractedNode, shortCuts)
    right = unpack_shortcut(contractedNode, current, shortCuts)
    return left + [contractedNode] + right

def unpackPathCH(previous, startNode, endNode, shortCuts):
    path = []
    currentNode = endNode

    while currentNode != startNode:
        path.append(currentNode)
        parent = previous[currentNode]
        # Check if the edge (parent, currentNode) is a shortcut
        sc_dict = shortCuts.get(parent)
        if currentNode in sc_dict.keys():
            sc = unpack_shortcut(parent, currentNode, shortCuts)

        path = path + sc[::-1]
        currentNode = parent

    path.append(startNode)
    return path[::-1]