import argparse
import heapq as hq
import time
from collections import OrderedDict
from queue import PriorityQueue
import sys
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from common.utility import GetPath
from common.Dijkstra import dijkstra
from common.A_star import a_star

if __name__ == "__main__":
    STARTTIME = time.time()
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--start-node', dest='STARTNODE', help='Wanted start node.', required=True)
    parser.add_argument('--end-node', dest='ENDNODE', help='Wanted end node.', required=True)
    parser.add_argument('--country', dest='COUNTRY', required=True)
    parser.add_argument('--algorithm', dest='ALGORITHM', required=True)
    args = parser.parse_args()

    STARTTIME = time.time()

    FILEPATH = f'../data/processed'
    FOLDERNAME = args.COUNTRY.lower()
    wantedStartNode = int(args.STARTNODE)
    wantedEndNode = int(args.ENDNODE)
    algorithm = args.ALGORITHM.lower()
    
    algorithms = {'dijkstra':dijkstra, 'a_star':a_star}
    
    
    
            
    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'
            
    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=float)
            
    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=int)
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=int)
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=float)
              
    
    
    
    
    distancesDict, previousDict = algorithms[algorithm](E, V, W, lat, lon, wantedStartNode, wantedEndNode)
    
    
    
    
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
        

    cmap = matplotlib.cm.Blues(np.linspace(0,1,128))
    cmap = matplotlib.colors.ListedColormap(cmap[10:,:-1])      
    cmap.set_under('grey')
    #plt.colorbar(cmap)
    plt.rcParams['figure.dpi'] = 400


    plt.suptitle(f'{wantedStartNode} ⇒ {wantedEndNode}', fontweight = 'bold', horizontalalignment = 'center')



    if positionsOfNodesInShortesPath:
        plt.title(f'Total travel distance: {totalDistance}km', style = 'italic', fontsize = 12, loc = 'center')
    else:
        plt.title(f'Found no path', style = 'italic')
    plt.scatter(lon, lat, s = 0.05, c = distances, cmap = cmap, vmin = 0)
    plt.plot(*zip(*positionsOfNodesInShortesPath), linewidth = 0.5, linestyle = 'dashed', color = 'black')
    plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], c = 'green', s = 2)
    plt.scatter(wantedEndNodeCoords[0], wantedEndNodeCoords[1], c = 'red', s = 2)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar()
    plt.savefig(f'../data/plots/{FOLDERNAME}/{algorithm}_myPlot.png')

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')

    