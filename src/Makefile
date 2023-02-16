## Preprocessing

get_nodes_in_highways:
	python 01_preprocessing/01_get_nodes_in_highways.py --raw-data-destination ${FILENAME}

get_positions_of_nodes:
	python 01_preprocessing/02_get_positions_of_nodes.py --raw-data-destination ${FILENAME}

create_plot:
	python 01_preprocessing/03_create_plot.py

get_edges:
	python 01_preprocessing/04_get_edges.py --raw-data-destination ${FILENAME}

get_distances:
	python 01_preprocessing/05_get_distances_of_edges.py

preprocessing: get_nodes_in_highways get_positions_of_nodes create_plot get_edges get_distances

## Shortest Path



# start = 1528652289
# end = 10275888659
dijkstra:
	python 02_dijkstra/dijkstra.py --start-node ${STARTNODE} --end-node ${ENDNODE}
