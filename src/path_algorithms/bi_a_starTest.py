import pickle
import numpy as np
import random
import time



from algorithms.Bidirectional_A_Star import bidirectional_a_star

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
    print(f'Loaded Lat and Lon')



    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()
    queries = queries[:100]

    bi_aStarTimes = []
    bi_aStarVisited = []

    for startNode, endNode in queries:
                
        STARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = bidirectional_a_star(E, V, W, E_rev, V_rev, W_rev, lat, lon, startNode, endNode)
        ENDTIME = time.time()
        
        bi_aStarTimes.append(ENDTIME - STARTTIME)
        bi_aStarVisited.append(len(forwardDistances) + len(backwardDistances))
                
    
    np.savetxt('bi_aStarTimes.txt', bi_aStarTimes, fmt='%f')
    np.savetxt('bi_aStarVisited.txt', bi_aStarVisited, fmt='%i')


