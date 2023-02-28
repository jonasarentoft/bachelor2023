import argparse
import heapq as hq
import time
from collections import OrderedDict
from queue import PriorityQueue
import sys
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import datashader as ds
import colorcet as cc
from PIL import Image as im



from common.utility import GetPath

from common.Dijkstra import dijkstra
from common.A_star import a_star
from common.Bidirectional import bidirectional
from common.Bidirectional_A_Star import bidirectional_a_star


if __name__ == "__main__":
    STARTTIME = time.time()
    # Handle arguments 
    parser = argparse.ArgumentParser(description='Specify wanted start node.')
    parser.add_argument('--start-node', dest='STARTNODE', help='Wanted start node.', required=True)
    parser.add_argument('--end-node', dest='ENDNODE', help='Wanted end node.', required=True)
    parser.add_argument('--country', dest='COUNTRY', required=True)
    parser.add_argument('--algorithm', dest='ALGORITHM', required=True)
    args = parser.parse_args()

    STARTTIME = time.time()

    FILEPATH = f'../data/processed'
    FOLDERNAME = args.COUNTRY.lower()
    wantedStartNode = int(args.STARTNODE)
    wantedEndNode = int(args.ENDNODE)
    algorithm = args.ALGORITHM.lower()
    
    algorithms = {'dijkstra':dijkstra, 
                  'a_star':a_star, 
                  'bidirectional':bidirectional,
                  'bidirectional_a_star':bidirectional_a_star}
    
    
    
    
    
            
    file = f'{FILEPATH}/{FOLDERNAME}/nodesAndPositions.txt'
            
    lat, lon = np.loadtxt(file, delimiter=',', usecols=(2, 3), unpack=True, dtype=np.float32)
        
    df = pd.DataFrame({'x': lon, 'y': lat})
        
    
    E = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E.txt', dtype=int)
    V = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V.txt', dtype=int)
    W = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W.txt', dtype=float)
    
    if algorithm in ['bidirectional', 'bidirectional_a_star']:
        E_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/E_reversed.txt', dtype=int)
        V_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/V_reversed.txt', dtype=int)
        W_rev = np.loadtxt(f'{FILEPATH}/{FOLDERNAME}/W_reversed.txt', dtype=float)
        ALGORITMSTARTTIME = time.time()
        nodesInShortestPath, distancesDict = algorithms[algorithm](E, V, W, E_rev, V_rev, W_rev, lat, lon, wantedStartNode, wantedEndNode)
        ALGORITMENDTIME = time.time()
        
    else:
        ALGORITMSTARTTIME = time.time()
        distancesDict, previousDict = algorithms[algorithm](E, V, W, lat, lon, wantedStartNode, wantedEndNode)
        ALGORITMENDTIME = time.time()
        
        nodesInShortestPath = GetPath(wantedEndNode, previousDict)
    
    
    TOTALALGORITHMTIME = round(ALGORITMENDTIME - ALGORITMSTARTTIME, 3)
    print(f'Took {TOTALALGORITHMTIME} seconds to run path find algorithm \n')
    distances = [distancesDict.get(ID, -1) for ID in range(len(V))]
    #coords = nodesAndPositions.values()
    wantedStartNodeCoords = [lon[wantedStartNode], lat[wantedStartNode]]
    wantedEndNodeCoords = [lon[wantedEndNode], lat[wantedEndNode]]
    positionsOfNodesInShortesPath = [[lon[node], lat[node]] for node in nodesInShortestPath]
    
    positionsOfNodesInShortesPathDF = pd.DataFrame(positionsOfNodesInShortesPath, columns = ['x', 'y'], dtype=np.float32)
    if positionsOfNodesInShortesPath:
        print('-->','Path found')
        totalDistance = distancesDict.get(wantedEndNode)
        totalDistance = round(totalDistance, 3)
        

    # cmap = matplotlib.cm.Blues(np.linspace(0,1,128))
    # cmap = matplotlib.colors.ListedColormap(cmap[10:,:-1])      
    # cmap.set_under('grey')
    # #plt.colorbar(cmap)
    # plt.rcParams['figure.dpi'] = 400


    # plt.suptitle(f'{wantedStartNode} ⇒ {wantedEndNode}', fontweight = 'bold', horizontalalignment = 'center')



    # if positionsOfNodesInShortesPath:
    #     plt.title(f'Total travel distance: {totalDistance}km', style = 'italic', fontsize = 12, loc = 'center')
    # else:
    #     plt.title(f'Found no path', style = 'italic')
    # plt.scatter(lon, lat, s = 0.05, c = distances, cmap = cmap, vmin = 0)
    # plt.plot(*zip(*positionsOfNodesInShortesPath), linewidth = 0.5, linestyle = 'dashed', color = 'black')
    # plt.scatter(wantedStartNodeCoords[0], wantedStartNodeCoords[1], c = 'green', s = 2)
    # plt.scatter(wantedEndNodeCoords[0], wantedEndNodeCoords[1], c = 'red', s = 2)
    # plt.xlabel('Longitude')
    # plt.ylabel('Latitude')
    # plt.colorbar()
    
    maxLat = max(lat)
    minLat = min(lat)
    maxLon = max(lon)
    minLon = min(lon)
    
    
    cvs = ds.Canvas(plot_width=3000, plot_height=3000, x_range=(minLon, maxLon), y_range=(minLat, maxLat))
    cv1 = ds.Canvas(plot_width=3000, plot_height=3000, x_range=(minLon, maxLon), y_range=(minLat, maxLat))# auto range or provide the `bounds` argument
    agg = cvs.points(df, 'x', 'y')  # this is the histogram
    agg1 = cv1.line(positionsOfNodesInShortesPathDF, 'x', 'y', line_width=5)  # this is the histogram
    
    img = ds.tf.set_background(ds.tf.shade(agg, how="cbrt", cmap=cc.fire), "black")#.to_pil() # create a rasterized image
    
    path = ds.tf.set_background(ds.tf.shade(agg1, how="log", cmap=cc.fire), "black")#.to_pil() # create a rasterized image
    
    
    # newImage = []
    # for item in path.getdata():
    #     if item[:3] == (0, 0, 0):
    #         newImage.append((0, 0, 0, 0))
    #     else:
    #         newImage.append(item)

    # path.putdata(newImage)
    
    

    # im.alpha_composite(img, path).save("test3.png")

    # img.save("test.png", "PNG")
    

    #img.paste(asd)
    
    stacked = ds.tf.stack(img, path)
    
    plt.rcParams['figure.dpi'] = 2400
    plt.imshow(stacked)
    plt.axis('off')

    
    plt.savefig(f'../data/plots/{FOLDERNAME}/{algorithm}_myPlot.png', bbox_inches='tight', dpi = 2400)

    ENDTIME = time.time()
    TOTALTIME = round(ENDTIME - STARTTIME, 3)
    print(f'Took {TOTALTIME} seconds to run \n')

    