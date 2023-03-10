import argparse
import os
import time
import xml.etree.ElementTree as ET
import numpy as np

from common.DistanceFormula import DistanceFormula

from datetime import datetime

if __name__ == "__main__":
    STARTTIME = time.time()

    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()
    
    FILEPATH = f'../data/processed'
    FOLDERNAME = args.FILENAME.split(".")[0]


    with open(f"{FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt", "r") as edgesAndDistances:
        with open(f"{FILEPATH}/{FOLDERNAME}/E_reversed.txt", "w") as E:
            with open(f"{FILEPATH}/{FOLDERNAME}/V_reversed.txt", "w") as V:
                with open(f"{FILEPATH}/{FOLDERNAME}/W_reversed.txt", "w") as W:
        
                    previousNode = -1

                    totalCount = 0
                    for line in edgesAndDistances:
                    
                        toNode, fromNode, distance = line.strip().split(',')
                        fromNode = int(fromNode)
                        
                        while fromNode - np.abs(previousNode) > 1:
                            V.write(f'{totalCount}\n')
                            previousNode +=1

                        if fromNode == previousNode:
                            E.write(f'{toNode}\n')
                            W.write(f'{distance}\n')
                            totalCount += 1
                        
                        else:
                            V.write(f'{totalCount}\n')
                            E.write(f'{toNode}\n')
                            W.write(f'{distance}\n')
                            totalCount += 1
                            previousNode = fromNode
                    V.write(f'{totalCount}\n')
                            
        
        
    print('færdig. husk at sortere nu')
       # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt /o {FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt')

    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt -o {FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt')
                            
    with open(f"{FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt", "r") as edgesAndDistances:
        with open(f"{FILEPATH}/{FOLDERNAME}/E.txt", "w") as E:
            with open(f"{FILEPATH}/{FOLDERNAME}/V.txt", "w") as V:
                with open(f"{FILEPATH}/{FOLDERNAME}/W.txt", "w") as W:
        
                    previousNode = -1

                    totalCount = 0
                    for line in edgesAndDistances:
                        
                        fromNode, toNode, distance = line.strip().split(',')
                        fromNode = int(fromNode)
                        
                        while fromNode - np.abs(previousNode) > 1:
                            V.write(f'{totalCount}\n')
                            previousNode +=1
        

                        if fromNode == previousNode:
                            E.write(f'{toNode}\n')
                            W.write(f'{distance}\n')
                            totalCount += 1
                            
                        
                        else:
                            V.write(f'{totalCount}\n')
                            E.write(f'{toNode}\n')
                            W.write(f'{distance}\n')
                            totalCount += 1
                            previousNode = fromNode
                    V.write(f'{totalCount}\n')
                            
                            
                            
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')
    
    
    CURRENTTIME = datetime.now().strftime("%H:%M:%S")
    print(f'Pipeline started at {CURRENTTIME}\n')