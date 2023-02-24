import argparse
import os
import time
import xml.etree.ElementTree as ET
import numpy as np

from common.DistanceFormula import DistanceFormula

from datetime import datetime

if __name__ == "__main__":
    STARTTIME = time.time()


    # Specify path to processed data
    FILEPATH = f'../data/processed'

    with open(f"{FILEPATH}/edgesWithDistances.txt", "r") as edgesAndDistances:
        with open(f"{FILEPATH}/E.txt", "w") as E:
            with open(f"{FILEPATH}/V.txt", "w") as V:
                with open(f"{FILEPATH}/W.txt", "w") as W:
        
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
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')
    
    
    CURRENTTIME = datetime.now().strftime("%H:%M:%S")
    print(f'Pipeline started at {CURRENTTIME}\n')