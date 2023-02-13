import argparse
import time
import xml.etree.ElementTree as ET

from common.BinarySearch import (BinarySearchIndex,  # Custom functions
                                 BinarySearchTF)

#################################################################################  

# SCRIPT FOR CREATING nodesAndPositions.txt FILE
# nodeID, lat, lon

#################################################################################

if __name__ == "__main__":
    STARTTIME = time.time()
    
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Get raw data.')
    parser.add_argument('--raw-data-destination', dest='FILENAME', help='Name of file in the data folder.', required=True)
    args = parser.parse_args()

    # Specify path to processed data
    FILEPATH = f'../data/processed'
    

    


    # Løb filerne igennem sideløbende så vi ikke læser node id's ind i hukommelsen
    with open(f'{FILEPATH}/nodesInHighwaysSorted.txt', 'r') as nodes:
        with open(f'{FILEPATH}/nodesAndPositions.txt', 'w') as f:
            tree = ET.iterparse(f'../data/raw/{args.FILENAME}', events = ('start', 'end'))


            for node in nodes:
                node_found = False
                for event, child in tree:

                    if event == 'start':

                        if child.tag == 'node':
                        
                            if child.attrib['id'] == node.strip():  
                                node_found = True
                                nodeID = child.attrib['id']
                                lat = child.attrib['lat']
                                lon = child.attrib['lon']

                                f.write(f'{nodeID}, {lat}, {lon}\n')
                                break

                    if event == 'end':
                        child.clear()
                        
                if node_found:
                    continue
                                
                                    
                    
                        
            ENDTIME = time.time()
    
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')