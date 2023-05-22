import heapq as hq
import sys
import numpy as np

def GetPath(target, previousDict):
    previous = previousDict.get(target)
    
    previous = previousDict.get(target)
    path = [target]
    while previous:
        path = path + [previous]
        previous = previousDict.get(previous)
    return path
        

def get_sizes(tree, r, weights, landmarks):
    sizes = {}

    children = tree.get(r)

    if not children:
        if r in landmarks:
            sizes[r] = 0
        else:
            sizes[r] = weights[r]
        return sizes

    for child in children:
        dictionary = get_sizes(tree, child, weights, landmarks)
        sizes.update(dictionary)
        if min(sizes.get(child), sizes.get(r, np.nan)) == 0:
            sizes[r] = 0
        else:
            sizes[r] = sizes.get(r, weights[r]) + sizes.get(child)
    
    return sizes

        
def create_tree(previousDict):
    tree = {}
    
    for key in previousDict.keys():
        parent = previousDict.get(key)
        tree[parent] = tree.get(parent, []) + [key]
    return tree


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
    