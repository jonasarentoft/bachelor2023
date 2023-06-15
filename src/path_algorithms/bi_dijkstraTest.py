import pickle
import numpy as np
import random
import time



from algorithms.Bidirectional import bidirectional

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



    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()

    bi_dijkstraTimes = []
    bi_dijkstraVisited = []

    for startNode, endNode in queries:
                
        STARTTIME = time.time()
        forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection = bidirectional(E, V, W, E_rev, V_rev, W_rev, 0, 0, startNode, endNode)
        ENDTIME = time.time()
        
        bi_dijkstraTimes.append(ENDTIME - STARTTIME)
        bi_dijkstraVisited.append(len(forwardDistances) + len(backwardDistances))
                

                    
                    
                    
    np.savetxt('bi_dijkstraTimes.txt', bi_dijkstraTimes, fmt='%f')
    np.savetxt('bi_dijsktraVisited.txt', bi_dijkstraVisited, fmt='%i')


