import argparse
import os
import time
import xml.etree.ElementTree as ET

from common.DistanceFormula import DistanceFormula

if __name__ == "__main__":
    STARTTIME = time.time()
    
    # Handle arguments 

    
    FILEPATH = f'../data/processed'

    with open(f'{FILEPATH}/edgesWithPartialCoords.txt', 'w') as f:
        
        with open(f'{FILEPATH}/edgesSorted.txt', 'r') as edges:

            with open(f'{FILEPATH}/nodesAndPositions.txt', 'r') as nodesAndPos:

                nodeID, lat, lon = nodesAndPos.readline().strip('\n').split(',')
                nodeID = int(nodeID.strip())


                for edge in edges:
                    nodeOne, nodeTwo = edge.strip('\n').split(',')
                    nodeOneInt = int(nodeOne.strip())
                    while nodeOneInt > nodeID:
                        try:
                            nodeID, lat, lon = nodesAndPos.readline().strip('\n').split(',')
                            nodeID = int(nodeID.strip())
                        except:
                            break
                    
                  
                    f.write(f'{nodeOne},{nodeTwo},{lat},{lon}\n')       

        # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/edgesWithPartialCoords.txt /+12 /o {FILEPATH}/edgesWithPartialCoordsSorted.txt')

    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/edges.txt -o -n {FILEPATH}/edgesSorted.txt')


    with open(f'{FILEPATH}/edgesWithDistances.txt', 'w') as f:
        
        with open(f'{FILEPATH}/edgesWithPartialCoordsSorted.txt', 'r') as edges:

            with open(f'{FILEPATH}/nodesAndPositions.txt', 'r') as nodesAndPos:

                nodeID, lat2, lon2 = nodesAndPos.readline().strip('\n').split(',')
                nodeID = int(nodeID.strip())

                for edge in edges:
                    nodeOne, nodeTwo, lat1, lon1 = edge.strip('\n').split(',')
                    nodeTwoInt = int(nodeTwo.strip())
                    while nodeTwoInt > nodeID:
                        try:
                            nodeID, lat2, lon2 = nodesAndPos.readline().strip('\n').split(',')
                            nodeID = int(nodeID.strip())
                        except:
                            break
                    
                    # Distance Formula
                    lat1 = float(lat1)
                    lat2 = float(lat2)
                    lon1 = float(lon1)
                    lon2 = float(lon2)
                    distance = DistanceFormula(lat1, lat2, lon1, lon2)
                    
                    nodeOne = nodeOne.strip()
                    nodeTwo = nodeTwo.strip()

                    f.write(f'{nodeOne},{nodeTwo},{distance}\n')
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')