# visit_most_node_device(process_dict)

# G,node_dict,count = dict_to_graph_networkx(process_dict)
# G = dict_to_graph_graphviz(process_dict)

# for key in node_dict.keys():
	# 	x.append(key)
	# 	y.append(node_dict[key] / float(count[key]))
    
    # remove certain values in process_dict
	# count_big = 0
	# count_small = 0
	# for key in time_duration_hist.keys():
	# 	if key > 720:
	# 		count_big += 1
	# 		del time_duration_hist[key]
	# 	else:
	# 		if key > 100:
	# 			count_small += 1
	# 			del time_duration_hist[key]

	# maximum = max(time_duration_hist, key=time_duration_hist.get)  # Just use 'min' instead of 'max' for minimum.
	# print(maximum, time_duration_hist[maximum])

	# with open("time_duration_hist20180722.txt",'w') as f:
	# 	for key in time_duration_hist.keys():
	# 		if key > 720:
	# 			print >> f,time_duration_hist[key]

	
	# nx.write_gexf(G,"graph20180722.gexf")

	# with open("individual_20180722.txt",'w') as fp:
	# 	# print >>fp,stop_time_dict
	# 	for target_device in process_dict.keys():
	# 		fp.write("%s device \n" % target_device)
	# 		print >> fp,sorted(process_dict[target_device].items(), key=lambda x: x[0])

	# 		# print >>fp,stop_time_dict[target_device]
	# 		fp.write("-----------------------------\n")