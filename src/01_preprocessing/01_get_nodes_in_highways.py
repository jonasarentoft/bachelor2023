import argparse
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from bz2file import BZ2File
import sys


import numpy as np

#################################################################################  

# SCRIPT FOR CREATING nodesInHighways.txt FILE
# nodeID

#################################################################################

if __name__ == "__main__":
    CURRENTTIME = datetime.now().strftime("%H:%M:%S")
    print(f'Pipeline started at {CURRENTTIME}\n')
    
    
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()

    # Specify path to processed data
    FILEPATH = f'../data/processed'
    FOLDERNAME = args.FILENAME.split(".")[0]
    
    FOLDERPATH = f'{FILEPATH}/{FOLDERNAME}'
    
    PATHEXISTS = os.path.exists(FOLDERPATH)
        
    if not PATHEXISTS:
        # Create a new directory because it does not exist
        os.makedirs(FOLDERPATH)
    

    with open(f'{FILEPATH}/{FOLDERNAME}/nodesInHighways.txt', 'w') as f:
        
        print(f'../data/raw/{args.FILENAME}')
        with BZ2File(f'../data/raw/{args.FILENAME}') as xml_file:

        
            tree = ET.iterparse(xml_file, events = ('start', 'end'))
            
            
            
            for event, child in tree:
                if event == 'start':
                    if child.tag == 'way':
                        highway = [grandchild.attrib['k'] == 'highway' for grandchild in child if grandchild.tag == 'tag']
                        nodes = [grandchild.attrib['ref'] for grandchild in child if grandchild.tag == 'nd']

                        if any(highway):
                            print('her')
                            for node in nodes:
                                ws = " " * (12 - len(str(node)))
                                f.write(f'{ws}{node}\n')
                                print(ws)
                                
                if event == 'end':
                    child.clear()

    # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/{FOLDERNAME}/nodesInHighways.txt  /unique /o {FILEPATH}/{FOLDERNAME}/nodesInHighwaysSorted.txt')

    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/{FOLDERNAME}/nodesInHighways.txt --unique -o {FILEPATH}/{FOLDERNAME}/nodesInHighwaysSorted.txt')
        
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')