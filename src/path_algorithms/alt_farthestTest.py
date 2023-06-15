import pickle
import numpy as np
import random
import time



from algorithms.ALT import alt
if __name__ == "__main__":

    FILEPATH = f'../data/processed'
    FOLDERNAME = f'denmark'

    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype= np.int32)
    print(f'Loaded Edges')
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=np.int32)
    print(f'Loaded Vertices')
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)


    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'

    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)

    distancesToLandmarks = {}
    distancesFromLandmarks = {}
    N = 20

    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()

    altTimes = []
    altVisited = []


    fileName = F'{FILEPATH}/{FOLDERNAME}/landmarks_farthest'
    for i in range(N):
        distancesToLandmarks[i] = np.loadtxt(f'{fileName}/L{i}.txt', delimiter=',', usecols=(1), unpack=True, dtype=np.float32)
        print(f'Loaded Distances to Landmarks for landmark {i}')
        distancesFromLandmarks[i] = np.loadtxt(f'{fileName}/L{i}.txt', delimiter=',', usecols=(0), unpack=True, dtype=np.float32)
        print(f'Loaded Distances from Landmarks for landmark {i}')
    for startNode, endNode in queries:
        STARTTIME = time.time()
        distancesDict, previousDict = alt(E, V, W, lat, lon, startNode, endNode, distancesToLandmarks, distancesFromLandmarks)
        ENDTIME = time.time()
        altTimes.append(ENDTIME - STARTTIME)
        altVisited.append(len(distancesDict))

    np.savetxt('alt_farthestTimes.txt', altTimes, fmt='%f')
    np.savetxt('alt_farthestVisited.txt', altVisited, fmt='%i')

        
