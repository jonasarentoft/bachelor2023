import time

import matplotlib.pyplot as plt
import numpy as np

#################################################################################  

# SCRIPT FOR CREATING PLOT OF HIGHWAY NODES

#################################################################################

if __name__ == "__main__":
    STARTTIME = time.time()
    FILEPATH = f'../data/processed'

    coords = []
    with open(f'{FILEPATH}/nodesAndPositions.txt', 'r') as nodes:

        for line in nodes:
            list = [float(i) for i in line.strip().split(sep=",")]
            coords.append(list[1:])


    X = np.array(coords)
    plt.plot(X[:, 1], X[:, 0], 'o', markersize=0.1)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.axis('equal')
    plt.savefig(f'../data/plots/plot.png')
    
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')