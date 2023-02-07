import argparse
import os
import time
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np

from common.BinarySearch import BinarySearchIndex  # Custom functions
from common.BinarySearch import BinarySearchTF
from common.DistanceFormula import DistanceFormula

#################################################################################  

# SCRIPT FOR CREATING edges.txt FILE
# FROM, TO, DISTANCE

#################################################################################

if __name__ == "__main__":
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()
    
    FILEPATH = f'../data/processed'

    with open(f'{FILEPATH}/nodesAndPositions.txt', 'r') as n:
        nodes = []
        lats = []
        longs = []

        for line in n.readlines():
            node, lat, lon = line.strip('\n').split(',')
            nodes.append(int(node))
            lats.append(float(lat))
            longs.append(float(lon))
    
    with open(f'{FILEPATH}/edges.txt', 'w') as f:
            
            tree = ET.iterparse(f'../data/raw/{args.FILENAME}', events = ('start', 'end'))
            for event, child in tree:
                if event == 'start':
                    if child.tag == 'way':
                        child_attributes = child.attrib
                        
                        highway = any([grandchild.attrib['k'] == 'highway' for grandchild in child if grandchild.tag == 'tag'])
                        nds = [grandchild.attrib['ref'] for grandchild in child if grandchild.tag == 'nd']
                        twoway = not any([grandchild.attrib['k'] == 'oneway' and grandchild.attrib['v'] == 'yes' for grandchild in child if grandchild.tag == 'tag'])

                        if highway:
                            for i in range(len(nds) - 1):

                                nodeOne = nds[i].strip()
                                nodeTwo = nds[i + 1].strip()
                                
                                lineNodeOne = BinarySearchIndex(nodes, int(nodeOne))
                                lineNodeTwo = BinarySearchIndex(nodes, int(nodeTwo))

                                latNodeOne = lats[lineNodeOne]
                                lonNodeOne = longs[lineNodeOne]
                                latNodeTwo = lats[lineNodeTwo]
                                lonNodeTwo = longs[lineNodeTwo]

                                # Distance Formula
                                distance = DistanceFormula(latNodeOne, latNodeTwo, lonNodeOne, lonNodeTwo)

                                f.write(f'{nodeOne},{nodeTwo},{distance}\n') # (from, to)

                                if twoway:
                                    f.write(f'{nodeTwo},{nodeOne},{distance}\n') # (from, to)
                                
                if event == 'end':
                    child.clear()
                    
                    
    # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/edges.txt /unique /o {FILEPATH}/edgesSorted.txt')

    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/edges.txt --unique -o {FILEPATH}/edgesSorted.txt')
                                    
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')