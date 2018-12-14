from collections import Counter
# plot top 10(or whatever number) classical individual trajectories in gephi
def plot_popular_individual(time_duration,process_dict):
	# get device list
	popular_device = dict(Counter(time_duration).most_common(5))
	popular_dict = {}
	for key in popular_device.keys():
		popular_dict[key] = process_dict[key]
	G, _, _ = dict_to_graph_networkx(popular_dict)
	pos = nx.spring_layout(G)
	nodes = G.nodes()
	edges = G.edges()
	weights = [G[u][v]['weight'] for u,v in edges]
	colors = [G[u][v]['color'] for u,v in edges]
	# nx.draw(G, pos, nodes = nodes,edges = edges, edge_color = colors, width = weights)
	labels = {}
	for node in G.nodes():
		labels[node] = node
	ec = nx.draw_networkx_edges(G, pos, edge_color = colors, width = weights,alpha=0.2)
	nc = nx.draw_networkx_nodes(G, pos, nodelist=nodes, with_labels=True, node_size=100)
	lc = nx.draw_networkx_labels(G, pos, labels, font_size=16)
	plt.show()
	nx.write_gexf(G,"forty_most_popular.gexf",version="1.2draft")
	return G

def plot_popular_individual_graphviz(time_duration,process_dict):
	popular_device = dict(Counter(time_duration).most_common(5))
	popular_dict = {}
	for key in popular_device.keys():
		popular_dict[key] = process_dict[key]
	G = dict_to_graph_graphviz(popular_dict)
	G.layout()
	G.draw('pgv_5_trajectory_parallel_between_buildings_20180804.png')
	return G

# print popular devices in terminal for further Matlab processing
# thresh: time duration threshold, add node_num to trajectory_dict if larger than thresh
def print_popular_individual(process_dict,thresh=0):
	# popular_device = dict(Counter(metric).most_common(len(metric.keys())))
	
	# least_popular_devices = sorted(metric, key=metric.__getitem__)[0:1000]

	# popular_dict = {}
	# popular_dict = copy.deepcopy(process_dict)

	# for i in range(0,1000):
	# 	popular_dict[least_popular_devices[i]] = process_dict[least_popular_devices[i]]

	# for key in popular_device.keys():
	# 	# node_num = process_dict[key].keys()[0]
	# 	popular_dict[key] = process_dict[key]
		# sort in ascending order of key 
		# sort_list = sorted(popular_dict[key].items(), key=lambda x: x[0])

		# print the node number (817, {24: 3}) --> print out 24
		# print sort_list[0][1].keys()
		# print sort_list
	trajectory_dict = {}
	for device in process_dict.keys():
		trajectory_dict[device] = []
		keylist = process_dict[device].keys()
		keylist.sort(key=int)
		for key in keylist:
			for node_num in process_dict[device][key].keys():
				if process_dict[device][key][node_num] > thresh:
					trajectory_dict[device].append(node_num)
		# if trajectory_dict[device] == [], delete entry
		if not trajectory_dict[device]:
			del trajectory_dict[device]

	return trajectory_dict