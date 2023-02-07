import pandas as pd
from common.utility import Node

if __name__ == "__main__":
    x = 3

    edgesSorted = pd.read_csv('../data/processed/edgesSorted.txt', 
                              names = ['from', 'to', 'distance'])
    
    
    nodesInHighways = pd.read_csv('../data/processed/nodesInHighwaysSorted.txt', 
                                  names = ['ID'])
    
    
    
    myNodes = {}

    for _, row in nodesInHighways.iterrows():
        ID = row['ID']
        myNodes[ID] = Node(ID)
        
        
    for i, row in edgesSorted.iterrows():    
        fromID = row['from']
        toID = row['to']
        distance = row['distance']
        
        fromNode = myNodes[fromID]
        toNode =  myNodes[toID]
        
        Node.add_edge(fromNode, toNode, distance)
    
        
        
    