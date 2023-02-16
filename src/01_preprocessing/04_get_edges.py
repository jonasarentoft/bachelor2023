import argparse
import os
import time
import xml.etree.ElementTree as ET
from bz2file import BZ2File
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

    

        
    
    with open(f'{FILEPATH}/edges.txt', 'w') as f:
        
        
        with BZ2File(f'../data/raw/{args.FILENAME}') as xml_file:

        
            tree = ET.iterparse(xml_file, events = ('start', 'end'))
        

            for event, child in tree:
                if event == 'start':
                    if child.tag == 'way':
                        child_attributes = child.attrib
                        
                        highway = any([grandchild.attrib['k'] == 'highway' for grandchild in child if grandchild.tag == 'tag'])
                        nds = [grandchild.attrib['ref'] for grandchild in child if grandchild.tag == 'nd']
                        twoway = not any([grandchild.attrib['k'] == 'oneway' and grandchild.attrib['v'] == 'yes' for grandchild in child if grandchild.tag == 'tag'])
                        
                        if highway:
                            for i in range(len(nds) - 1):
                                nodeOne = nds[i]
                                nodeTwo = nds[i + 1]
                                
                                wsOne = " " * (12 - len(nodeOne))
                                wsTwo = " " * (12 - len(nodeTwo))
                                f.write(f'{wsOne}{nodeOne},{wsTwo}{nodeTwo}\n') # (from, to)

                                if twoway:
                                    f.write(f'{wsTwo}{nodeTwo},{wsOne}{nodeOne}\n') # (from, to)
                        
                    

                                
                if event == 'end':
                    child.clear()
                    
                    
    # Windows/Linux
    if os.name == 'nt':
        os.system(f'cmd /c SORT {FILEPATH}/edges.txt /o {FILEPATH}/edgesSorted.txt')

    # MAC
    elif os.name == 'posix':
        os.system(f'SORT {FILEPATH}/edges.txt -o {FILEPATH}/edgesSorted.txt')
                                    
    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')