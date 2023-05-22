import time

import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

#################################################################################  

# SCRIPT FOR CREATING PLOT OF HIGHWAY NODES

#################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()

    STARTTIME = time.time()
    FILEPATH = f'../data/processed'
    PLOTPATH = f'../data/plots'
    FOLDERNAME = args.FILENAME.split(".")[0]
    
    PLOTPATH = f'{PLOTPATH}/{FOLDERNAME}'
    
    PATHEXISTS = os.path.exists(PLOTPATH)
    
    if not PATHEXISTS:
        # Create a new directory because it does not exist
        os.makedirs(PLOTPATH)
    

    coords = []
    with open(f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt', 'r') as nodes:

        for line in nodes:
            list = [float(i) for i in line.strip().split(sep=",")]
            coords.append(list[2:])


    X = np.array(coords)
    plt.rcParams['figure.dpi'] = 600
    plt.plot(X[:, 1], X[:, 0], 'o', markersize=0.1)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(f'../data/plots/{FOLDERNAME}/plot.png')
    
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')