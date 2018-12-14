from distance_calc import distance_match, square_difference
# spot the most popular pair to extract betweenness, e.g. 5->12
def plot_popular_pair(trajectory_dict):
	pair_count = {}
	for device in trajectory_dict.keys():
		node_list = trajectory_dict[device]
		for i in range(0,len(node_list) - 1):
			pair_string = str(node_list[i]) + '->' + str(node_list[i + 1])
			if pair_string not in pair_count.keys():
				pair_count[pair_string] = 1
			else:
				pair_count[pair_string] += 1
	return pair_count

# count in_degree and out_degree of each node
def count_degree(pair_count):
	# count in_degree
	in_connect = {}
	out_connect = {}

	for pair in pair_count.keys():
		in_node, out_node = pair.split("->")
		in_node = int(in_node)
		out_node = int(out_node)
		if in_node not in in_connect.keys():
			in_connect[in_node] = pair_count[pair]
		elif in_node in in_connect.keys():
			in_connect[in_node] += pair_count[pair]
		if out_node not in out_connect.keys():
			out_connect[out_node] = pair_count[pair]
		elif out_node in out_connect.keys():
			out_connect[out_node] += pair_count[pair]

	return in_connect,out_connect

# set threshold to pairs
def set_threshold(pair_count, thresh):
	popular_count = {}
	for pair in pair_count.keys():
		in_node, out_node = pair.split("->")
		in_node = int(in_node)
		out_node = int(out_node)
		if square_difference(distance_match(in_node),distance_match(out_node)) >= thresh:
			popular_count[pair] = pair_count[pair]
	return popular_count

# count flow every 2 nodes
def count_flow(node,pair_count):
	flow = {}
	for node_i in node:
		for node_j in node:
			node_tuple = (node_i,node_j)
			flow[node_tuple] = 0
			flow[node_tuple] += count_flow_helper(node_i,node_j,pair_count)
	return flow



# count flow between i and j(gij)
def count_flow_helper(node_i,node_j,pair_count):
	count = 0
	pair_string = str(node_i) + '->' + str(node_j)
	pair_string_1 = str(node_j) + '->' + str(node_i)
	if pair_string in pair_count.keys():
		count += pair_count[pair_string]
	if pair_string_1 in pair_count.keys():
		count += pair_count[pair_string_1]
	return count

# count outflow every 2 nodes
def count_outflow(node,pair_count):
	outflow = {}
	for node_i in node:
		outflow[node_i] = 0
		for node_j in [node_num for node_num in node if node_num!=node_i]:
			outflow[node_i] += count_outflow_helper(node_i,node_j,pair_count)
	return outflow
	
# count outflow from node_i to node_j
def count_outflow_helper(node_i,node_j,pair_count):
	count = 0
	pair_string = str(node_i) + '->' + str(node_j)
	if pair_string in pair_count.keys():
		count += pair_count[pair_string]
	return count
