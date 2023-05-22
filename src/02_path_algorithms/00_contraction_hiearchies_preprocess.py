import argparse
import os
import time
from datetime import datetime
import heapq as hq
import numpy as np
import pickle

from common.algorithms.DijkstraCHpreprocess import dijkstra, initOrder, lazyUpdate
        
if __name__ == "__main__":
    CURRENTTIME = datetime.now().strftime("%H:%M:%S")
    print(f'Pipeline started at {CURRENTTIME}\n')
    
    
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--country', dest='COUNTRY', required=True)
    args = parser.parse_args()

    # Specify path to processed data
    FILEPATH = f'../data/processed'
    FOLDERNAME = args.COUNTRY.lower()
    FOLDERPATH = f'{FILEPATH}/{FOLDERNAME}/contractionHiearchies'
    PATHEXISTS = os.path.exists(FOLDERPATH)
    if not PATHEXISTS:
        # Create a new directory because it does not exist
        os.makedirs(FOLDERPATH)




    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=int)
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=int)
    Weights = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)
    print('Loaded V, E, W')
    E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
    V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
    Weights_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
    print('Loaded V, E, W Reversed')
    
    printEvery = int(len(V)/10)
    progress = 0

    shortCuts = {}
    shortCuts_rev = {}
    for i in range(len(V)-1):
        shortCuts[i] = {}
        shortCuts_rev[i] = {}
    numOfShortCuts = 0
    distDict = {}
    prio = {}


    nodeOrdering = initOrder(V, E, Weights, V_rev, E_rev, Weights_rev, shortCuts)
    print('Initial node ordering created')
    reOrder = 0
    i = 0

    while nodeOrdering:
        _, v = hq.heappop(nodeOrdering)
        vShortCutDict = shortCuts.get(v)
        vShortCutDict_rev = shortCuts_rev.get(v)
        prio[v] = i
        v_orderPrio, U, W, dijkstraResults = lazyUpdate(prio, v, vShortCutDict, vShortCutDict_rev, V, E, Weights, V_rev, E_rev, Weights_rev, shortCuts)
        if nodeOrdering:
            nextMin = nodeOrdering[0][0]
            if nextMin < v_orderPrio:
                prio.pop(v)
                reOrder += 1
                hq.heappush(nodeOrdering, (v_orderPrio, v))
                continue

        if U and W:
            for u, W_u in U:
                
                distDict = dijkstraResults.get(u)
                for j, (w, W_w) in enumerate(W):
                    if distDict.get(w) == None or distDict.get(w) > W_u + W_w:
                        shortCuts[u][w] = (v, W_u + W_w)
                        shortCuts_rev[w][u] = (v, W_u + W_w)
                        numOfShortCuts += 1
        if i % printEvery == 0:
            print(f'{progress}% contracted')
            progress += 10           
        i += 1


    print(f'Finished contracting')
    print(f'Added {numOfShortCuts} shortcuts')

    print('Saving Dictionaries')
    with open(f'{FOLDERPATH}/prio.pkl', 'wb') as f:
        pickle.dump(prio, f)
    with open(f'{FOLDERPATH}/shortCuts.pkl', 'wb') as f:
        pickle.dump(shortCuts, f)
    with open(f'{FOLDERPATH}/shortCuts_rev.pkl', 'wb') as f:
        pickle.dump(shortCuts_rev, f)
    print('Dictionaries saved')
    ENDTIME = time.time()
    print(f'took {ENDTIME - STARTTIME} seconds')