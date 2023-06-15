import argparse
import heapq as hq
import time
from collections import OrderedDict
from queue import PriorityQueue
import sys
import matplotlib.colors
import matplotlib.pyplot as plt
from datashader.utils import export_image
import matplotlib
import numpy as np
import pandas as pd
import datashader as ds
import colorcet as cc
from PIL import Image as im
from functools import wraps
import time
import _pickle as cPickle

from common.GetPath import GetPath
from common.GetPathCH import getIntersectNodeCH, unpack_shortcut, unpackPathCH

#from algorithms.CH import dijkstraCH
from algorithms.Dijkstra import dijkstra
from algorithms.A_star import a_star
from algorithms.Bidirectional import bidirectional
from algorithms.Bidirectional_A_Star import bidirectional_a_star
from algorithms.ALT import alt
from algorithms.Bidirectional_ALT import bidirectional_alt
from algorithms.Bidirectional_CH import bidirectional_CH

from common.GetAddress import GetAddress
from common.GetDataForBidrectional import GetDataForBidirectional

if __name__ == "__main__":
    STARTTIME = time.time()
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--start-node', dest='STARTNODE', help='Wanted start node.', required=True)
    parser.add_argument('--end-node', dest='ENDNODE', help='Wanted end node.', required=True)
    parser.add_argument('--country', dest='COUNTRY', required=True)
    parser.add_argument('--algorithm', dest='ALGORITHM', required=True)
    parser.add_argument('--N', dest='N', const = 20, nargs='?')
    parser.add_argument('--landmarks', dest='LANDMARKS', const = 'farthest', nargs='?')
    args = parser.parse_args()

    STARTTIME = time.time()
    
    LANDMARKS = args.LANDMARKS
    
    #FILEPATH = f'../data/processed'
    #FOLDERNAME = args.COUNTRY.lower()

    FILEPATH = '/volumes/T7/jonas_bachelor2023'
    FOLDERNAME = 'europe_data'
    
    wantedStartNode = int(args.STARTNODE)
    wantedEndNode = int(args.ENDNODE)
    specifiedAlgorithm = args.ALGORITHM.lower()
    algorithms = {'dijkstra':dijkstra, 
                  'a_star':a_star, 
                  'bidirectional':bidirectional,
                  'bidirectional_a_star':bidirectional_a_star,
                  'alt':alt,
                  'bidirectional_alt':bidirectional_alt,
                  'ch':bidirectional_CH}
    
    
    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'
            
    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)
    print(f'Loaded Lat and Lon')
    print(round(time.time() - STARTTIME, 3))
        
    df = pd.DataFrame({'x': lon, 'y': lat})
    
    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=np.int32)
    print(f'Loaded Edges')
    print(round(time.time() - STARTTIME, 3))
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=np.int32)
    print(f'Loaded Vertices')
    print(round(time.time() - STARTTIME, 3))
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)
    print(f'Loaded Weights')
    print(round(time.time() - STARTTIME, 3))
    rs = []
    landmarks = []




#[107386, 28219, 41438, 135921, 46909, 150934, 147721, 75, 148848, 103426]
    
    if specifiedAlgorithm in ['bidirectional', 'bidirectional_a_star']:
        E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
        print(f'Loaded Reversed Edges')
        V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
        print(f'Loaded Reversed Vertices')
        W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
        print(f'Loaded Reversed Weights')
        ALGORITMSTARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = algorithms[specifiedAlgorithm](E, V, W, E_rev, V_rev, W_rev, lat, lon, wantedStartNode, wantedEndNode)
        ALGORITMENDTIME = time.time()

        
        distancesDict, nodesInShortestPath, totalDistance  = GetDataForBidirectional(forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection)

        
    elif specifiedAlgorithm in ['dijkstra', 'a_star']:
        ALGORITMSTARTTIME = time.time()
        distancesDict, forwardPrevious = algorithms[specifiedAlgorithm](E, V, W, lat, lon, wantedStartNode, wantedEndNode)
        ALGORITMENDTIME = time.time()
        
        
        nodesInShortestPath = GetPath(wantedEndNode, forwardPrevious)
        totalDistance = distancesDict.get(wantedEndNode)
    
    
    elif specifiedAlgorithm in ['alt', 'bidirectional_alt']:
        N = int(args.N)
        distancesToLandmarks = {}
        distancesFromLandmarks = {}
        fileName = f'{FILEPATH}/{FOLDERNAME}/landmarks_{LANDMARKS}'
        
        landmarks = np.array(np.loadtxt(f'{fileName}/landmarkIDs.txt', dtype=int))[0:N]
        
        if LANDMARKS == 'avoid':
            rs = np.array(np.loadtxt(f'{fileName}/rs.txt', dtype=int))[0:N]
        
        
        for i in range(N):
            distancesToLandmarks[i] = np.loadtxt(f'{fileName}/L{i}.txt', delimiter=',', usecols=(1), unpack=True, dtype=np.float32)
            print(f'Loaded Distances to Landmarks for node {i}')
            distancesFromLandmarks[i] = np.loadtxt(f'{fileName}/L{i}.txt', delimiter=',', usecols=(0), unpack=True, dtype=np.float32)
            print(f'Loaded Distances from Landmarks for node {i}')
            
        if specifiedAlgorithm == 'alt':
            
            ALGORITMSTARTTIME = time.time()
            distancesDict, forwardPrevious = algorithms[specifiedAlgorithm](E, V, W, lat, lon, wantedStartNode, wantedEndNode, distancesToLandmarks, distancesFromLandmarks)
            ALGORITMENDTIME = time.time()
            
            nodesInShortestPath = GetPath(wantedEndNode, forwardPrevious)
            totalDistance = distancesDict.get(wantedEndNode)
                
        else:
            E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
            print(f'Loaded Reversed Edges')
            V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
            print(f'Loaded Reversed Vertices')
            W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
            print(f'Loaded Reversed Weights')
            
            
            forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = algorithms[specifiedAlgorithm](E, V, W, E_rev, V_rev, W_rev, wantedStartNode, wantedEndNode, distancesToLandmarks, distancesFromLandmarks)
            
            distancesDict, nodesInShortestPath, totalDistance  = GetDataForBidirectional(forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection)
            
    elif specifiedAlgorithm == 'ch':

        E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
        print(f'Loaded Reversed Edges')
        V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
        print(f'Loaded Reversed Vertices')
        W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
        print(f'Loaded Reversed Weights')

        fileName = F'{FILEPATH}/{FOLDERNAME}/contraction_hiearchies'
        
        
        with open(f'{fileName}/prio.pkl', 'rb') as f:
            prio = cPickle.load(f)
        print(f'Loaded prio')
        with open(f'{fileName}/shortCuts.pkl', 'rb') as f:
            shortCuts = cPickle.load(f)
        print(f'Loaded shortCuts')
        with open(f'{fileName}/shortCuts_rev.pkl', 'rb') as f:
            shortCuts_rev = cPickle.load(f)
        print(f'Loaded Reversed shortCuts')


        ALGORITMSTARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = bidirectional_CH(E, V, W, E_rev, V_rev, W_rev, shortCuts, shortCuts_rev, wantedStartNode, wantedEndNode, prio)
        ALGORITMENDTIME = time.time()

        totalDistance = forwardDistances[intersection] + backwardDistances[intersection]

        pathForward = unpackPathCH(forwardPrevious, wantedStartNode, intersection, shortCuts)
        pathBackward = unpackPathCH(backwardPrevious, wantedEndNode, intersection, shortCuts_rev)
        
        nodesInShortestPath = pathForward + pathBackward[::-1]
        
        
        distancesDict, shortCutPath, b = GetDataForBidirectional(forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection)
        positionsOfNodesInShortCutPath = [[lon[node], lat[node]] for node in shortCutPath]
        positionsOfNodesInShortCutPathDF = pd.DataFrame(positionsOfNodesInShortCutPath, columns = ['x', 'y'], dtype=np.float32)
        
        

    print(f'Number of nodes in shortest path: {len(nodesInShortestPath)}({specifiedAlgorithm})')
    
    distances = [distancesDict.get(ID, -1) for ID in range(len(V))]
    
    
    positionsOfNodesInShortesPath = [[lon[node], lat[node]] for node in nodesInShortestPath]
    positionsOfNodesInShortesPathDF = pd.DataFrame(positionsOfNodesInShortesPath, columns = ['x', 'y'], dtype=np.float32)
    if positionsOfNodesInShortesPath:
        print('-->','Path found')
        try:
            totalDistance = round(totalDistance, 3)
        except:
            totalDistance = 0
    
    
    
    maxLat = max(lat)
    minLat = min(lat)
    maxLon = max(lon)
    minLon = min(lon)
    
    newMaxLat = maxLat #+ 0.2
    newMinLat = minLat #- 0.2
    newMaxLon = maxLon #+ 0.2
    newMinLon = minLon #- 0.2
    
    
    xScaler = 3000 / (newMaxLon - newMinLon)
    yScaler = 3000 / (newMaxLat - newMinLat)
                
    
    landmarkspos = [[lon[node], lat[node]] for node in landmarks]
    
    randomxs = [xScaler * (x - newMinLon) for [x, _] in landmarkspos]
    randomys = [3000 - yScaler * (y - newMinLat) for [_, y] in landmarkspos]
    
    
    rpos = [[lon[node], lat[node]] for node in rs]
    rposx = [xScaler * (x - newMinLon) for [x, _] in rpos]
    rposy = [3000 - yScaler * (y - newMinLat) for [_, y] in rpos]
    

    wantedStartNodeCoords = [xScaler * (lon[wantedStartNode] - newMinLon), 3000 - yScaler * (lat[wantedStartNode] - newMinLat)]
    wantedEndNodeCoords = [xScaler * (lon[wantedEndNode] - newMinLon), 3000 - yScaler * (lat[wantedEndNode] - newMinLat)]
    
    startAndEndPoints = pd.DataFrame([wantedStartNodeCoords, wantedEndNodeCoords], columns = ['x', 'y'])
    
    
    
    
    cvs = ds.Canvas(plot_width=3000, plot_height=3000, x_range=(newMinLon, newMaxLon), y_range=(newMinLat, newMaxLat))
    agg = cvs.points(df, 'x', 'y')  # this is the histogram
    agg1 = cvs.line(source = positionsOfNodesInShortesPathDF, x = 'x', y = 'y', line_width=10)#, line_width=5)
    
    img = ds.tf.shade(agg, how="log", cmap=cc.gray)
    path = ds.tf.shade(agg1, cmap=cc.CET_C5s)
    
    if not specifiedAlgorithm in ['bidirectional', 'bidirectional_alt', 'bidirectional_a_star']:
        points = np.array([(lon[id], lat[id]) for id in distancesDict.keys()])
        searchedPoints = pd.DataFrame(points, columns = ['x', 'y'])
        agg2 = cvs.points(searchedPoints, 'x', 'y')
        searched = ds.tf.shade(agg2, how="eq_hist", cmap=cc.kg)
        
    else:
        forwardPoints = np.array([(lon[id], lat[id]) for id in forwardDistances.keys()])
        searchedForwardPoints = pd.DataFrame(forwardPoints, columns = ['x', 'y'])
        agg3 = cvs.points(searchedForwardPoints, 'x', 'y')
        
        backwardPoints = np.array([(lon[id], lat[id]) for id in backwardDistances.keys()])
        searchedBackwardPoints = pd.DataFrame(backwardPoints, columns = ['x', 'y'])
        agg4 = cvs.points(searchedBackwardPoints, 'x', 'y')
        
        
        forwardSearched = ds.tf.shade(agg3, how="eq_hist", cmap=cc.kg)
        backwardSearched = ds.tf.shade(agg4, how="eq_hist", cmap=cc.kr)
        searched = ds.tf.stack(forwardSearched, backwardSearched)


    stacked = ds.tf.stack(img, searched, path)
    stacked = ds.tf.set_background(stacked, "white").to_pil()



    implot = plt.imshow(stacked)
    plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], color = 'green', s = 10, edgecolors = 'black', linewidths = 0.5)
    plt.annotate('s', (wantedStartNodeCoords[0], wantedStartNodeCoords[1]), size=3, ha='center', va = 'center', color = 'white')
    plt.scatter(wantedEndNodeCoords[0],wantedEndNodeCoords[1], color = 'red', s = 10, edgecolors = 'black', linewidths = 0.5)
    plt.annotate('t', (wantedEndNodeCoords[0], wantedEndNodeCoords[1]), size=3, ha='center', va = 'center', color = 'white')

    plt.scatter(randomxs, randomys, color = 'orange', s = 17, marker="D", edgecolors = 'orange', linewidth = 0.2)
    #plt.xlim(0.00001,5)
    #plt.scatter(rposx, rposy, color = 'pink', s = 8, marker="D", edgecolors = 'black', linewidth = 0.2)
    n = range(1, len(randomxs)+1)
    for i, number in enumerate(n):
        plt.annotate(number, (randomxs[i], randomys[i]), size=3, ha='center', va = 'center', color ='white')
    #    if LANDMARKS == 'avoid':
            #plt.annotate(number, (rposx[i], rposy[i]), size=2, ha='center', va = 'center', color = 'white')
    
    plt.gcf().set_facecolor("white")
    plt.axis('off')
    #plt.suptitle(f'{wantedStartNode} ⇒ {wantedEndNode}', fontweight = 'bold', horizontalalignment = 'center', color = 'black')

    # if positionsOfNodesInShortesPath:
    #     plt.title(f'Total travel distance: {totalDistance}km', style = 'italic', fontsize = 12, loc = 'center', color ='black')
    # else:
    #     plt.title(f
    # 'Found no path', style = 'italic',color ='black')
    #plt.xlim(-100, 2000)
    #plt.ylim(3100, -100)

    
    plt.savefig(f'../data/plots/{FOLDERNAME}/{specifiedAlgorithm}.png', bbox_inches='tight', dpi = 3000)

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    TOTALALGORITHMTIME = round(ALGORITMENDTIME - ALGORITMSTARTTIME, 3)
    
    try:
        no = len(forwardDistances + backwardDistances)
    except Exception:
        no = len(distancesDict)
    print(f'Took {TOTALTIME} seconds to run\n Algorithm took {TOTALALGORITHMTIME} seconds to run\n Total number of visited nodes is {no}')