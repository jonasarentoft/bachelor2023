## Preprocessing

get_nodes_in_highways:
	python preprocessing/01_get_nodes_in_highways.py --raw-data-destination ${FILENAME}

get_positions_of_nodes:
	python preprocessing/02_get_positions_of_nodes.py --raw-data-destination ${FILENAME}

create_plot:
	python preprocessing/03_create_plot.py --raw-data-destination ${FILENAME}

get_edges:
	python preprocessing/04_get_edges.py --raw-data-destination ${FILENAME}

get_distances:
	python preprocessing/05_get_distances_of_edges.py --raw-data-destination ${FILENAME}

create_il:
	python preprocessing/06_create_incidence_lists.py --raw-data-destination ${FILENAME}

preprocessing: get_nodes_in_highways get_positions_of_nodes create_plot get_edges get_distances create_il

## Shortest Path

create_farthest:
	python create_landmarks/01_farthest.py --country ${COUNTRY} --number-of-landmarks ${N}

create_avoid:
	python create_landmarks/02_avoid.py --country ${COUNTRY} --number-of-landmarks ${N}

contraction_preprocess:
	python contraction_hiearchies/01_ch_preprocess.py --country ${COUNTRY}
# start = 1528652289
# end = 10275888659



dijkstra:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm dijkstra

bidirectional:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm bidirectional

a_star:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm a_star

bidirectional_a_star:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm bidirectional_a_star

alt:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --N ${N} --landmarks ${LANDMARKS} --algorithm alt 

bidirectional_alt:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --N ${N} --landmarks ${LANDMARKS} --algorithm bidirectional_alt 

bidirectional_ch:
	python path_algorithms/01_run_path_algorithm.py --start-node ${STARTNODE} --end-node ${ENDNODE} --country ${COUNTRY} --algorithm ch


plot:
	python path_algorithms/02_plot_results.py --country ${COUNTRY}

run_all: dijkstra bidirectional a_star bidirectional_a_star alt bidirectional_alt bidirectional_ch


### Benchmarking
make_queries:
	python path_algorithms/makeQueries.py

dijkstra_benchmark:
	python path_algorithms/dijkstraTest.py

dijkstra_early_benchmark:
	python path_algorithms/dijkstra_earlyTest.py

bi_dijkstra_benchmark:
	python path_algorithms/bi_dijkstraTest.py

a_star_benchmark:
	python path_algorithms/a_starTest.py

bi_a_star_benchmark:
	python path_algorithms/bi_a_starTest.py

alt_avoid_benchmark:
	python path_algorithms/alt_avoidTest.py

bi_alt_avoid_benchmark:
	python path_algorithms/bi_alt_avoidTest.py

alt_farthest_benchmark:
	python path_algorithms/alt_farthestTest.py

bi_alt_farthest_benchmark:
	python path_algorithms/bi_alt_farthestTest.py

ch_benchmark:
	python path_algorithms/chTest.py

run_all_benchmarks: dijkstra_benchmark dijkstra_early_benchmark bi_dijkstra_benchmark a_star_benchmark bi_a_star_benchmark alt_avoid_benchmark bi_alt_avoid_benchmark alt_farthest_benchmark bi_alt_farthest_benchmark ch_benchmark

run_alt: bi_alt_avoid_benchmark bi_alt_farthest_benchmark


