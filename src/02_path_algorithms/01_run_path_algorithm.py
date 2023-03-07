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
import datashader as ds
import colorcet as cc
from PIL import Image as im

from common.utility import GetPath

from common.Dijkstra import dijkstra
from common.A_star import a_star
from common.Bidirectional import bidirectional
from common.Bidirectional_A_Star import bidirectional_a_star

from common.GetAddress import GetAddress
from common.GetDataForBidrectional import GetDataForBidirectional

from scipy.spatial import ConvexHull


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

    #FILEPATH = '/volumes/T7/jonas_bachelor2023'
    #FOLDERNAME = 'europe_data'
    
    wantedStartNode = int(args.STARTNODE)
    wantedEndNode = int(args.ENDNODE)
    algorithm = args.ALGORITHM.lower()
    
    algorithms = {'dijkstra':dijkstra, 
                  'a_star':a_star, 
                  'bidirectional':bidirectional,
                  'bidirectional_a_star':bidirectional_a_star}
    
    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'
            
    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)
    print(f'Loaded Lat and Lon')
        
    df = pd.DataFrame({'x': lon, 'y': lat})
    
    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=int)
    print(f'Loaded Edges')
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=int)
    print(f'Loaded Vertices')
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)
    print(f'Loaded Weights')
    
    if algorithm in ['bidirectional', 'bidirectional_a_star']:
        E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
        print(f'Loaded Reversed Edges')
        V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
        print(f'Loaded Reversed Vertices')
        W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
        print(f'Loaded Reversed Weights')
        
        ALGORITMSTARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious = algorithms[algorithm](E, V, W, E_rev, V_rev, W_rev, lat, lon, wantedStartNode, wantedEndNode)
        ALGORITMENDTIME = time.time()
        
        distancesDict, nodesInShortestPath = GetDataForBidirectional(forwardDistances, backwardDistances, forwardPrevious, backwardPrevious)
        
    else:
        ALGORITMSTARTTIME = time.time()
        distancesDict, previousDict = algorithms[algorithm](E, V, W, lat, lon, wantedStartNode, wantedEndNode)
        ALGORITMENDTIME = time.time()
        
        nodesInShortestPath = GetPath(wantedEndNode, previousDict)
        
    print(f'Number of nodes in shortest path: {len(nodesInShortestPath)}({algorithm})')
    file = open(f'{algorithm}.txt','w')
    for item in nodesInShortestPath:
        file.write(str(item) + ',')
    file.close()
    
    TOTALALGORITHMTIME = round(ALGORITMENDTIME - ALGORITMSTARTTIME, 2)
    print(f'Took {TOTALALGORITHMTIME} seconds to run path find algorithm \n')
    
    distances = [distancesDict.get(ID, -1) for ID in range(len(V))]
    
    points = np.array([(lon[id], lat[id]) for id in distancesDict.keys()])

    positionsOfNodesInShortesPath = [[lon[node], lat[node]] for node in nodesInShortestPath]
    
    positionsOfNodesInShortesPathDF = pd.DataFrame(positionsOfNodesInShortesPath, columns = ['x', 'y'], dtype=np.float32)
    if positionsOfNodesInShortesPath:
        print('-->','Path found')
        totalDistance = distancesDict.get(wantedEndNode)
        try:
            totalDistance = round(totalDistance, 3)
        except:
            totalDistance = 0
    
    maxLat = max(lat) + 0.5
    minLat = min(lat) - 0.5
    maxLon = max(lon) + 0.5
    minLon = min(lon) - 0.5
    
    xScaler = 3000 / (maxLon - minLon)
    yScaler = 3000 / (maxLat - minLat)
    
    wantedStartNodeCoords = [xScaler * (lon[wantedStartNode] - minLon), 3000 - yScaler * (lat[wantedStartNode] - minLat)]
    wantedEndNodeCoords = [xScaler * (lon[wantedEndNode] - minLon), 3000 - yScaler * (lat[wantedEndNode] - minLat)]
    
    #startCity = GetAddress(lon[wantedStartNode], lat[wantedStartNode])
    #endCity = GetAddress(lon[wantedEndNode], lat[wantedEndNode]) 
    
    startAndEndPoints = pd.DataFrame([wantedStartNodeCoords, wantedEndNodeCoords], columns = ['x', 'y'])
    
    searchedPoints = pd.DataFrame(points, columns = ['x', 'y'])
    
    cvs = ds.Canvas(plot_width=3000, plot_height=3000, x_range=(minLon, maxLon), y_range=(minLat, maxLat))
    agg = cvs.points(df, 'x', 'y')  # this is the histogram
    agg1 = cvs.line(source = positionsOfNodesInShortesPathDF, x = 'x', y = 'y', line_width=5)#, line_width=5)
    agg2 = cvs.points(searchedPoints, 'x', 'y')
    
    img = ds.tf.shade(agg, how="cbrt", cmap=cc.fire)
    path = ds.tf.shade(agg1, how="log", cmap=cc.fire)
    searched = ds.tf.shade(agg2, how="log", cmap=cc.CET_C1s)
    
    stacked = ds.tf.stack(img, searched, path)
    stacked = ds.tf.set_background(stacked, "black").to_pil()

    implot = plt.imshow(stacked)
    
    plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], color = 'green', s = 4)
    plt.scatter(wantedEndNodeCoords[0],wantedEndNodeCoords[1], color = 'blue', s = 4)
    
    plt.gcf().set_facecolor("black")
    plt.axis('off')
    #plt.suptitle(f'{startCity} ({wantedStartNode}) ⇒ {endCity} ({wantedEndNode})', fontweight = 'bold', horizontalalignment = 'center', color = 'white')
    plt.suptitle(f'{wantedStartNode} ⇒ {wantedEndNode}', fontweight = 'bold', horizontalalignment = 'center', color = 'white')

    if positionsOfNodesInShortesPath:
        plt.title(f'Total travel distance: {totalDistance}km', style = 'italic', fontsize = 12, loc = 'center', color ='white')
    else:
        plt.title(f'Found no path', style = 'italic',color ='white')

    
    plt.savefig(f'../data/plots/{FOLDERNAME}/{algorithm}.png', bbox_inches='tight', dpi = 2400)

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')