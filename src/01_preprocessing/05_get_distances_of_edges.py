import argparse
import os
import time
import xml.etree.ElementTree as ET


from common.DistanceFormula import DistanceFormula

from datetime import datetime

if __name__ == "__main__":
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()
    
    FILEPATH = f'../data/processed'
    FOLDERNAME = args.FILENAME.split(".")[0]        

    with open(f'{FILEPATH}/{FOLDERNAME}/edgesWithPartialCoords.txt', 'w') as f:
        
        with open(f'{FILEPATH}/{FOLDERNAME}/edgesSorted.txt', 'r') as edges:

            with open(f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt', 'r') as nodesAndPos:

                id, nodeID, lat, lon = nodesAndPos.readline().strip('\n').split(',')
                nodeID = int(nodeID.strip())


                for edge in edges:
                    nodeOne, nodeTwo = edge.strip('\n').split(',')
                    nodeOneInt = int(nodeOne.strip())
                    
                    while nodeOneInt > nodeID:
                        try:
                            id, nodeID, lat, lon = nodesAndPos.readline().strip('\n').split(',')
                            nodeID = int(nodeID.strip())
                        except:
                            break
                    if nodeOneInt == nodeID:
                        f.write(f'{nodeOne},{nodeTwo},{id},{lat},{lon}\n')  
                         

    # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/{FOLDERNAME}/edgesWithPartialCoords.txt /+13 /o {FILEPATH}/{FOLDERNAME}/edgesWithPartialCoordsSorted.txt')


    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/{FOLDERNAME}/edgesWithPartialCoords.txt -t , -k2 -o {FILEPATH}/{FOLDERNAME}/edgesWithPartialCoordsSorted.txt')


    with open(f'{FILEPATH}/{FOLDERNAME}/edgesWithDistances.txt', 'w') as f:
        with open(f'{FILEPATH}/{FOLDERNAME}/edgesWithPartialCoordsSorted.txt', 'r') as edges:
            with open(f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt', 'r') as nodesAndPos:

                id, nodeID, lat2, lon2 = nodesAndPos.readline().strip('\n').split(',')
                nodeID = int(nodeID.strip())

                for edge in edges:
                    nodeOne, nodeTwo, idOne, lat1, lon1 = edge.strip('\n').split(',')
                    nodeTwoInt = int(nodeTwo.strip())
                    while nodeTwoInt > nodeID:
                        try:
                            id, nodeID, lat2, lon2 = nodesAndPos.readline().strip('\n').split(',')
                            nodeID = int(nodeID.strip())
                        except:
                            break
                    if nodeTwoInt == nodeID:
                        # Distance Formula
                        lat1 = float(lat1)
                        lat2 = float(lat2)
                        lon1 = float(lon1)
                        lon2 = float(lon2)
                        distance = DistanceFormula(lat1, lat2, lon1, lon2)
                        
                        nodeOne = nodeOne.strip()
                        nodeTwo = nodeTwo.strip()
                        ws = " " * (8 - len(idOne))
                        f.write(f'{ws}{idOne},{id},{distance}\n')

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')
    
    
    CURRENTTIME = datetime.now().strftime("%H:%M:%S")
    print(f'Pipeline started at {CURRENTTIME}\n')
    