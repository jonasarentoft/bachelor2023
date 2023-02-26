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
from common.utility import GetPath
from common.dijkstra import dijsktra

if __name__ == "__main__":
    STARTTIME = time.time()
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--start-node', dest='STARTNODE', help='Wanted start node.', required=True)
    parser.add_argument('--end-node', dest='ENDNODE', help='Wanted end node.', required=True)
    parser.add_argument('--country', dest='COUNTRY', required=True)
    args = parser.parse_args()

    STARTTIME = time.time()

    FILEPATH = f'../data/processed'
    FOLDERNAME = args.COUNTRY.lower()
    wantedStartNode = int(args.STARTNODE)
    wantedEndNode = int(args.ENDNODE)
    
            
    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'
            
    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=float)
            
    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=int)
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=int)
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=float)
              
    
    distancesDict, previousDict = dijkstra(E, V, W, wantedStartNode)
    distances = [distancesDict.get(ID, -1) for ID in range(len(V))]
    #coords = nodesAndPositions.values()
    wantedStartNodeCoords = [lon[wantedStartNode], lat[wantedStartNode]]
    wantedEndNodeCoords = [lon[wantedEndNode], lat[wantedEndNode]]
    nodesInShortestPath = GetPath(wantedEndNode, previousDict)
    positionsOfNodesInShortesPath = [[lon[node], lat[node]] for node in nodesInShortestPath]
    
    if positionsOfNodesInShortesPath:
        print('-->','Path found')
        totalDistance = distancesDict.get(wantedEndNode)
        totalDistance = round(totalDistance, 3)
        

    
    plt.rcParams['figure.dpi'] = 400


    plt.suptitle(f'{wantedStartNode} ⇒ {wantedEndNode}', fontweight = 'bold', horizontalalignment = 'center')



    if positionsOfNodesInShortesPath:
        plt.title(f'Total travel distance: {totalDistance}km', style = 'italic', fontsize = 12, loc = 'center')
    else:
        plt.title(f'Found no path', style = 'italic')
    plt.scatter(lon, lat, s = 0.05, c = distances)
    plt.plot(*zip(*positionsOfNodesInShortesPath), linewidth = 0.5, color = 'red')
    plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], c = 'red')
    plt.scatter(wantedEndNodeCoords[0], wantedEndNodeCoords[1], c = 'blue')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar()
    plt.savefig(f'../data/plots/{FOLDERNAME}/myPlot.png')

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')

    