import pickle
import numpy as np
import random
import time



from algorithms.Bidirectional_ALT import bidirectional_alt

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

    distancesToLandmarks = {}
    distancesFromLandmarks = {}
    N = 20

    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()

    altTimes = []
    altVisited = []


    fileName = F'{FILEPATH}/{FOLDERNAME}/landmarks_avoid'
    for i in range(N):
        distancesToLandmarks[i] = np.loadtxt(f'{fileName}/L{i}.txt', delimiter=',', usecols=(1), unpack=True, dtype=np.float32)
        print(f'Loaded Distances to Landmarks for landmark {i}')
        distancesFromLandmarks[i] = np.loadtxt(f'{fileName}/L{i}.txt', delimiter=',', usecols=(0), unpack=True, dtype=np.float32)
        print(f'Loaded Distances from Landmarks for landmark {i}')
        
    for startNode, endNode in queries:
        STARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = bidirectional_alt(E, V, W, E_rev, V_rev, W_rev, startNode, endNode, distancesToLandmarks, distancesFromLandmarks)
        ENDTIME = time.time()
        altTimes.append(ENDTIME - STARTTIME)
        altVisited.append(len(forwardDistances) + len(backwardDistances))

    np.savetxt('bi_alt_avoidTimes.txt', altTimes, fmt='%f')
    np.savetxt('bi_alt_avoidVisited.txt', altVisited, fmt='%i')

        
