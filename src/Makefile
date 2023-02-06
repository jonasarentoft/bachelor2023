get_nodes_in_highways:
	python 01_get_nodes_in_highways.py --raw-data-destination ${FILENAME}

get_positions_of_nodes:
	python 02_get_positions_of_nodes.py --raw-data-destination ${FILENAME}

create_plot:
	python 03_create_plot.py

get_edges:
	python 04_get_edges.py --raw-data-destination ${FILENAME}


pipeline: get_nodes_in_highways get_positions_of_nodes create_plot get_edges
	