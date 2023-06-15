import pickle
import numpy as np
import random
import time



from algorithms.Bidirectional_CH import bidirectional_CH
if __name__ == "__main__":

    FILEPATH = f'../data/processed'
    FOLDERNAME = f'denmark'

    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype= np.int32)
    print(f'Loaded Edges')
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=np.int32)
    print(f'Loaded Vertices')
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)

    E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=np.int32)
    V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=np.int32)
    W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=np.float32)
    print(f'Loaded Reversed lists')

    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'

    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)

    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()

    fileName = F'{FILEPATH}/{FOLDERNAME}/contractionHiearchies'
            
    with open(f'{fileName}/prio.pkl', 'rb') as f:
        prio = pickle.load(f)
    print(f'Loaded prio')
    with open(f'{fileName}/shortCuts.pkl', 'rb') as f:
        shortCuts = pickle.load(f)
    print(f'Loaded shortCuts')
    with open(f'{fileName}/shortCuts_rev.pkl', 'rb') as f:
        shortCuts_rev = pickle.load(f)
    print(f'Loaded Reversed shortCuts')

    algorithmTimes = []
    visitedNodes = []

    for startNode, endNode in queries:
        STARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = bidirectional_CH(E, V, W, E_rev, V_rev, W_rev, shortCuts, shortCuts_rev, startNode, endNode, prio)
        ENDTIME = time.time()
        algorithmTimes.append(ENDTIME - STARTTIME)
        visitedNodes.append(len(forwardDistances) + len(backwardDistances))
        
    np.savetxt('chTimes.txt', algorithmTimes, fmt='%f')
    np.savetxt('chVisited.txt', visitedNodes, fmt='%i')
