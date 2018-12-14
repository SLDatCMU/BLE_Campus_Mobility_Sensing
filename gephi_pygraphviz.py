import pygraphviz as pgv
import networkx as nx
def dict_to_graph_networkx(process_dict):
	G = nx.DiGraph()
	# {node_number: total staying time at each node}
	node_dict = {}
	total_node_list = []
	# count records how many visitors have visited each node
	count = {}
	for device in process_dict.keys():
		keylist = process_dict[device].keys()
		keylist.sort(key=int)
		# record the order of visited node
		node_list = []
		for key in keylist:
			for node_num in process_dict[device][key]:
				if node_num not in total_node_list:
					G.add_node(node_num, weight = process_dict[device][key][node_num])
					count[node_num] = 1
				else:
					G.nodes[node_num]['weight'] += process_dict[device][key][node_num]
					count[node_num] += 1
				total_node_list.append(node_num)
				node_list.append(node_num)
				if node_num not in node_dict.keys():
					node_dict[node_num] = process_dict[device][key][node_num]
				else:
					node_dict[node_num] += process_dict[device][key][node_num]

		for i in range(0,len(node_list) - 1):
			# if node_list[i] not in G.edges or node_list[i + 1] not in G.edges[node_list[i]]:
			G.add_edges_from([(node_list[i],node_list[i + 1])], weight = 1)
			#else:
			#G.edges[node_list[i]][node_list[i + 1]]['weight'] += 1
			
		# for i in range(0,len(node_list) - 1):
		# 	G.edges[node_list[i]][node_list[i+1]]['viz'] = {'color': {'r': 255, 'g': 0, 'b': 0, 'a': 0}}
	
	return G,node_dict,count

def dict_to_graph_graphviz(process_dict):
	G=pgv.AGraph(strict=False,directed=True)
	total_node_list = []
	total_edge_list = []
	# total_building_list = []
	# color = ['r','b','g','c','m','y','k']
	color = ['#808080', '#000000', '#FF0000', '#800000', '#FFFF00', 
						'#808000', '#00FF00', '#008000','#00FFFF','#008080','#0000FF','#000080','#FF00FF', '#800080']

	color_count = -1
	len_color = len(color)
	for device in process_dict.keys():
		color_count = (color_count + 1) % len_color 
		keylist = process_dict[device].keys()
		keylist.sort(key=int)
		# record the order of visited node
		node_list = []
		# building_list = []
		for key in keylist:
			for node_num in process_dict[device][key]:
				# building = group[node_num]
				if node_num not in total_node_list:
				# if building not in total_building_list:
					G.add_node(node_num, weight = process_dict[device][key][node_num])
					# G.add_node(building, weight = process_dict[device][key][node_num])
				else:
					# n = G.get_node(building)
					n = G.get_node(node_num)
					n.attr['weight'] = str(int(n.attr['weight']) + process_dict[device][key][node_num])
				total_node_list.append(node_num)
				node_list.append(node_num)
				# total_building_list.append(building)
				# building_list.append(building)
		for i in range(0,len(node_list) - 1):
			potential_edge = [node_list[i],node_list[i+1]]
			if potential_edge not in total_edge_list or G.get_edge(node_list[i],node_list[i+1]).attr['name'] != device:
				G.add_edge(node_list[i],node_list[i+1],color = color[color_count], weight = 1, name = device)
				total_edge_list.append(potential_edge)
		# for i in range(0,len(building_list) - 1):
		# 	potential_edge = [building_list[i],building_list[i+1]]
		# 	# skip same building edge
		# 	if building_list[i] == building_list[i + 1]:
		# 		continue
		# 	if potential_edge not in total_edge_list or G.get_edge(building_list[i],building_list[i+1]).attr['name'] != device:
		# 		G.add_edge(building_list[i],building_list[i+1], color = color[color_count], weight = 1, name = device)
		# 		total_edge_list.append(potential_edge)

	return G