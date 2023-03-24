## Preprocessing

get_nodes_in_highways:
	python 01_preprocessing/01_get_nodes_in_highways.py --raw-data-destination ${FILENAME}

get_positions_of_nodes:
	python 01_preprocessing/02_get_positions_of_nodes.py --raw-data-destination ${FILENAME}

create_plot:
	python 01_preprocessing/03_create_plot.py --raw-data-destination ${FILENAME}

get_edges:
	python 01_preprocessing/04_get_edges.py --raw-data-destination ${FILENAME}

get_distances:
	python 01_preprocessing/05_get_distances_of_edges.py --raw-data-destination ${FILENAME}

create_il:
	python 01_preprocessing/06_create_incidence_lists.py --raw-data-destination ${FILENAME}

preprocessing: get_nodes_in_highways get_positions_of_nodes create_plot get_edges get_distances create_il

## Shortest Path

create_landmarks:
	python 02_path_algorithms/00_landmarks_memoryEfficient.py --country ${COUNTRY} --number-of-landmarks ${N}


# start = 1528652289
# end = 10275888659



dijkstra:
	python 02_path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm dijkstra

bidirectional:
	python 02_path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm bidirectional

a_star:
	python 02_path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm a_star

bidirectional_a_star:
	python 02_path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm bidirectional_a_star

alt:
	python 02_path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --N ${N} --algorithm alt 

bidirectional_alt:
	python 02_path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --N ${N} --algorithm bidirectional_alt 


plot:
	python 02_path_algorithms/02_plot_results.py --country ${COUNTRY}

run_all: dijkstra bidirectional a_star bidirectional_a_star alt bidirectional_alt
