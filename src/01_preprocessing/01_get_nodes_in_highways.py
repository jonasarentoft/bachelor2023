import argparse
import os
import time
import xml.etree.ElementTree as ET

import numpy as np

#################################################################################  

# SCRIPT FOR CREATING nodesInHighways.txt FILE
# nodeID

#################################################################################

if __name__ == "__main__":
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()

    # Specify path to processed data
    FILEPATH = f'../data/processed'

    with open(f'{FILEPATH}/nodesInHighways.txt', 'w') as f:
        
        tree = ET.iterparse(f'../data/raw/{args.FILENAME}', events = ('start', 'end'))
        
        for event, child in tree:
            if event == 'start':
                if child.tag == 'way':
                    highway = [grandchild.attrib['k'] == 'highway' for grandchild in child if grandchild.tag == 'tag']
                    nodes = [grandchild.attrib['ref'] for grandchild in child if grandchild.tag == 'nd']

                    if any(highway):
                        for node in nodes:
                            f.write(f'{node}\n')
                            
            if event == 'end':
                child.clear()

    # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/nodesInHighways.txt /unique /o {FILEPATH}/nodesInHighwaysSorted.txt')

    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/nodesInHighways.txt --unique -o {FILEPATH}/nodesInHighwaysSorted.txt')
        
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')