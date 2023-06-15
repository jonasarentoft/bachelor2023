import pickle
import numpy as np
import random
import time



from algorithms.Dijkstra import dijkstra

if __name__ == "__main__":

    FILEPATH = f'../data/processed'
    FOLDERNAME = f'denmark'

    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype= np.int32)
    print(f'Loaded Edges')
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=np.int32)
    print(f'Loaded Vertices')
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=np.float32)



    queries = np.loadtxt('queries.txt', delimiter=' ', dtype=np.int32)
    queries = queries.tolist()

    dijkstraTimes = []
    dijkstraVisited = []

    for startNode, endNode in queries:
                
                STARTTIME = time.time()
                distancesDict, previousDict = dijkstra(E, V, W, 0, 0, startNode, endNode)
                ENDTIME = time.time()
                
                
                if distancesDict.get(endNode):
                    dijkstraTimes.append(ENDTIME - STARTTIME)
                    dijkstraVisited.append(len(distancesDict))
                    
                else:
                    queries.remove([startNode, endNode])
                    print(f'Removed {startNode} and {endNode}')
                    
                    
                    
    np.savetxt('dijsktraTimes.txt', dijkstraTimes, fmt='%f')
    np.savetxt('dijsktraVisited.txt', dijkstraVisited, fmt='%i')
    np.savetxt('queries.txt', queries, fmt='%i')

