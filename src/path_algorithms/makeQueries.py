import numpy as np
import random
import argparse


if __name__ == "__main__":
    
    N = 1000
    
    FILEPATH = f'../data/processed'
    FOLDERNAME = f'denmark'
    queries = []
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=np.int32)
    numberOfNodes = len(V) - 1
    for i in range(N):
        queries.append(random.sample(range(numberOfNodes), 2))
    np.savetxt('queries.txt', queries, fmt='%i')