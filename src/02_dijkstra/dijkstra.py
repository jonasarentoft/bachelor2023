import argparse
import heapq as hq
import time
from collections import OrderedDict
from queue import PriorityQueue
import sys
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common.utility import GetPath, dijkstra

if __name__ == "__main__":
    STARTTIME = time.time()
    sys.setrecursionlimit(5000)

    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--start-node', dest='STARTNODE', help='Wanted start node.', required=True)
    parser.add_argument('--end-node', dest='ENDNODE', help='Wanted end node.', required=True)
    args = parser.parse_args()

    STARTTIME = time.time()

    FILEPATH = f'../data/processed'
    wantedStartNode = int(args.STARTNODE)
    wantedEndNode = int(args.ENDNODE)

    nodesAndPositions = OrderedDict()

    with open(f'{FILEPATH}/nodesAndPositions.txt', 'r') as nodes:
        for line in nodes:
            list = [float(i) for i in line.split(sep=",")]
            # coords.append(list[1:])
            # nodeIDs.append(list[0])'
            
            nodesAndPositions[list[0]] = [list[3], list[2]]
            
            
    E = np.loadtxt(f"{FILEPATH}/E.txt", dtype=int)
    V = np.loadtxt(f"{FILEPATH}/V.txt", dtype=int)
    W = np.loadtxt(f"{FILEPATH}/W.txt", dtype=float)
            
            
    distancesDict, previousDict = dijkstra(E, V, W, wantedStartNode)
    print('-->',distancesDict.get(wantedEndNode))
    distances = [distancesDict.get(ID, -1) for ID in nodesAndPositions.keys()]
    coords = nodesAndPositions.values()
    wantedStartNodeCoords = nodesAndPositions[wantedStartNode]
    wantedEndNodeCoords = nodesAndPositions[wantedEndNode]
    print('-->',previousDict.get(wantedStartNode))
    nodesInShortestPath = GetPath(wantedEndNode, previousDict)
    print('-->','Path found')
    positionsOfNodesInShortesPath = [nodesAndPositions[node] for node in nodesInShortestPath]
    
    if positionsOfNodesInShortesPath:
        totalDistance = distancesDict.get(wantedEndNode)
        totalDistance = round(totalDistance, 3)
        

    
    plt.rcParams['figure.dpi'] = 400


    plt.suptitle(f'{wantedStartNode} ⇒ {wantedEndNode}', fontweight = 'bold', horizontalalignment = 'center')



    if positionsOfNodesInShortesPath:
        plt.title(f'Total travel distance: {totalDistance}km', style = 'italic', fontsize = 12, loc = 'center')
    else:
        plt.title(f'Found no path', style = 'italic')
    plt.scatter(*zip(*coords), s = 0.05, c = distances)
    plt.plot(*zip(*positionsOfNodesInShortesPath), linewidth = 0.5, color = 'red')
    plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], c = 'red')
    plt.scatter(wantedEndNodeCoords[0], wantedEndNodeCoords[1], c = 'blue')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar()
    plt.savefig('../data/plots/myPlot.png')

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')

    