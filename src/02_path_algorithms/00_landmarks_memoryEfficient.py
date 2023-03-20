import argparse
import os
import time
from datetime import datetime
import numpy as np
import pandas as pd
import random

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

    FILEPATH = f'../data/processed'
    FOLDERNAME = args.COUNTRY.lower()
    FOLDERPATH = f'{FILEPATH}/{FOLDERNAME}/landmarks'
    PATHEXISTS = os.path.exists(FOLDERPATH)
        
    if not PATHEXISTS:
        # Create a new directory because it does not exist
        os.makedirs(FOLDERPATH)



    numberOfLandmarks = int(args.N)
    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'
    

    
    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)
    print(f'Loaded Lat and Lon')
        
    df = pd.DataFrame({'x': lon, 'y': lat})
    
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
   
    for j in range(numberOfLandmarks):
        if j == 0: 
            startNode = random.randrange(numberOfVertices)
            currDists, _ = dijkstra(E, V, W, lat, lon, startNode, 0)

            firstLandmark = max(currDists, key = currDists.get)
            print('New landmark --> ', firstLandmark)

            currDists, _ = dijkstra(E, V, W, lat, lon, firstLandmark, 0)
            currDistsRev, _ = dijkstra(E_rev, V_rev, W_rev, lat, lon, firstLandmark, 0)
            with open(f'{FOLDERPATH}/L{j}.txt', 'w') as L:
                for i in range(numberOfVertices):
                    L.write(f'{currDists.get(i, "nan")},{currDistsRev.get(i, "nan")}\n')

        else:
            minDists = {}
            for l in range(j):
                file = f'{FOLDERPATH}/L{l}.txt'
                distances = np.loadtxt(file, delimiter=',', usecols=(1), unpack=True, dtype=np.float64)
                
                for i in range(numberOfVertices):
                    minDists[i] = min(distances[i], minDists.get(i, np.nan))

            newLandmark = max(minDists, key=minDists.get)
            print('New landmark --> ', newLandmark)
            currDists, currPrevs = dijkstra(E, V, W, lat, lon, newLandmark, 0)
            currDistsRev, _ = dijkstra(E_rev, V_rev, W_rev, lat, lon, newLandmark, 0)
            with open(f'{FOLDERPATH}/L{j}.txt', 'w') as L:
                for i in range(numberOfVertices):
                    L.write(f'{currDists.get(i, "nan")},{currDistsRev.get(i, "nan")}\n')

    ENDTIME = time.time()
    print(f'Took {ENDTIME - STARTTIME} seconds to run')
        
        


    