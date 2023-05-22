import argparse
import os
import time
from datetime import datetime
import numpy as np
import pandas as pd
import random
import sys

from common.utility import create_tree, get_sizes
from common.algorithms.Dijkstra import dijkstra 

if __name__ == "__main__":
    CURRENTTIME = datetime.now().strftime("%H:%M:%S")
    STARTTIME = time.time()
    print(f'Pipeline started at {CURRENTTIME}\n')
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--country', dest='COUNTRY', required=True)
    parser.add_argument('--number-of-landmarks', dest='N', required=True)
    args = parser.parse_args()

    sys.setrecursionlimit(6_000_000)

    FILEPATH = f'../data/processed'
    FOLDERNAME = args.COUNTRY.lower()
    FOLDERPATH = f'{FILEPATH}/{FOLDERNAME}/landmarksAvoid'
    PATHEXISTS = os.path.exists(FOLDERPATH)
        
    if not PATHEXISTS:
        # Create a new directory because it does not exist
        os.makedirs(FOLDERPATH)

    numberOfLandmarks = int(args.N)
    
    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=int)
    E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
    print(f'Loaded Edges')
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=int)
    V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
    print(f'Loaded Vertices')
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)
    W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
    print(f'Loaded Weights')
    
    numberOfVertices = len(V) - 1
    landmarks = []
   
    for j in range(numberOfLandmarks):
        r = random.randrange(numberOfVertices)
        if j == 0: 
            currDists, _ = dijkstra(E, V, W, 0, 0, r, 0)

            firstLandmark = max(currDists, key = currDists.get)
            landmarks.append(firstLandmark)
            print('New landmark --> ', firstLandmark)

            currDists, _ = dijkstra(E, V, W, 0, 0, firstLandmark, 0)
            currDistsRev, _ = dijkstra(E_rev, V_rev, W_rev, 0, 0, firstLandmark, 0)
            with open(f'{FOLDERPATH}/L{j}.txt', 'w') as L:
                for i in range(numberOfVertices):
                    L.write(f'{currDists.get(i, 0)},{currDistsRev.get(i, 0)}\n')

        else:
            minDists = {}
            weights = {}

            sizes = {}

            currDists, previousDict = dijkstra(E, V, W, 0, 0, r, 0)
            tree = create_tree(previousDict)

            # For l (landmark) in number of found landmarks
            for l in range(j):
                # file location for found landmark
                file = f'{FOLDERPATH}/L{l}.txt'
                # load distances from found landmark
                distancesFromLandmark = np.loadtxt(file, delimiter=',', usecols=(0), unpack=True, dtype=np.float64)
                distancesToLandmark = np.loadtxt(file, delimiter=',', usecols=(1), unpack=True, dtype=np.float64)
                
                # Calculate weight for every vertex, v, as 
                # min( dist*(r, v) - dist*(l, v) + dist*(l, r) ) for every l in S
                for i in range(numberOfVertices):
                    weights[i] = min(currDists.get(i, np.nan) - distancesFromLandmark[i] + distancesFromLandmark[r], weights.get(i, np.nan))
            print('--> weights calculated')
            # Calculate size(v) of every vertex where size(v) = 0 if T_v contains a landmark.
            # otherwise size(v) is the sum of weights of all vertices in T_v
            sizes = get_sizes(tree, r, weights, landmarks)
            print('--> sizes found')
            largestSubTree = max(sizes, key = sizes.get)
            children = tree[largestSubTree]

            while children:
                max(children, key = lambda x: sizes[x])
                newLST = max(children, key = lambda x: sizes[x])
                children = tree.get(newLST)
            
            newLandmark = newLST
            landmarks.append(newLandmark)
            print('New landmark --> ', newLandmark)
            currDists, currPrevs = dijkstra(E, V, W, 0, 0, newLandmark, 0)
            currDistsRev, _ = dijkstra(E_rev, V_rev, W_rev, 0, 0, newLandmark, 0)
            with open(f'{FOLDERPATH}/L{j}.txt', 'w') as L:
                for i in range(numberOfVertices):
                    L.write(f'{currDists.get(i, 0)},{currDistsRev.get(i, 0)}\n')
                    
    with open(f'{FOLDERPATH}/landmarkIDs.txt', 'w') as L:
                for landmark in landmarks:
                    L.write(f'{landmark}\n')


    ENDTIME = time.time()
    print(f'Took {ENDTIME - STARTTIME} seconds to run')
        
        


    