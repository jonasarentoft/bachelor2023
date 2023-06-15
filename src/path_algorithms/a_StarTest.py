import pickle
import numpy as np
import random
import time



from algorithms.A_star import a_star

if __name__ == "__main__":

    FOLDERNAME = f'denmark'
    FILEPATH = f'../data/processed'

    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype= np.int32)
    print(f'Loaded Edges')
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=np.int32)
    print(f'Loaded Vertices')
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)

    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'

    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)
    print(f'Loaded Lat and Lon')


    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()

    aStarTimes = []
    aStarVisited = []

    for startNode, endNode in queries:
        STARTTIME = time.time()
        distancesDict, previousDict = a_star(E, V, W, lat, lon, startNode, endNode)
        ENDTIME = time.time()
        

        aStarTimes.append(ENDTIME - STARTTIME)
        aStarVisited.append(len(distancesDict))

                    
                                    
    np.savetxt('aStarTimes.txt', aStarTimes, fmt='%f')
    np.savetxt('aStarVisited.txt', aStarVisited, fmt='%i')

