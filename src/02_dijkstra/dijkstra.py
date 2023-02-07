from queue import PriorityQueue
import pandas as pd
import heapq as hq
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors
from collections import OrderedDict
from common.utility import Node
from common.utility import dijkstra
import time
import argparse


if __name__ == "__main__":
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--start-node', dest='STARTNODE', help='Wanted start node.', required=True)
    args = parser.parse_args()

    STARTTIME = time.time()

    FILEPATH = f'../data/processed'
    wantedStartNode = int(args.STARTNODE)
    

    nodesAndPositions = OrderedDict()

    with open(f'{FILEPATH}/nodesAndPositions.txt', 'r') as nodes:
        for line in nodes:
            list = [float(i) for i in line.split(sep=",")]
            # coords.append(list[1:])
            # nodeIDs.append(list[0])'
            
            nodesAndPositions[list[0]] = [list[2], list[1]]
            
            
    myNodes = {}

    with open(f'{FILEPATH}/nodesInHighwaysSorted.txt', 'r') as nodes:
        for ID in nodes:
            ID = int(ID)
            myNodes[ID] = Node(ID)
        
            
            
    with open(f'{FILEPATH}/edgesSorted.txt', 'r') as edges:   
        for line in edges:
            data = [i for i in line.split(sep=",")]
            fromID, toID, distance = data        
            fromID = int(fromID)
            toID = int(toID)
            distance = float(distance)
            
            # Get Objects
            fromNode = myNodes[fromID]
            toNode =  myNodes[toID]
        
            Node.add_edge(fromNode, toNode, distance)
            
            
            
    dijkstra(myNodes[wantedStartNode])
    distances = [myNodes[ID].distance for ID in nodesAndPositions.keys()]
    coords = nodesAndPositions.values()
    wantedStartNodeCoords = nodesAndPositions[wantedStartNode]


    plt.rcParams['figure.dpi'] = 600
    plt.scatter(*zip(*coords), s = 0.05, c = distances)
    plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], c = 'red')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar()
    plt.savefig('../data/plots/myPlot.png')

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')
