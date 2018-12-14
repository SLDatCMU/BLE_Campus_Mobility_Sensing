from device_list_time_slot import get_device_list,get_device_single_node

node = [i for i in range(1,29) if i not in [2,11,17]]
# node = [i for i in range(1,29) if i not in [1,10,19,22,24,27,11,17]]

# device_list: list of list of dictionaries: [node],[time slot],{device uuid:device object}

# get_mini_length: avoid index out of range error
def get_mini_length(device_list):
	mini_length = len(device_list[0])
	for num in range(0,len(device_list)):
		if len(device_list[num]) < mini_length:
			mini_length = len(device_list[num])
	return mini_length

def get_connection(device_list):
	""" Get the connection relation and stopping time of each individual trajectory
	    Args: 
	        device_list: the list of list of dictionaries in devices
	    Returns:
		    dict of {time_slot: node number}
	"""
	node_number = node[0]
	mini_length = get_mini_length(device_list)
	# print mini_length

	# node_time_dict stores device uuid and which node number it appears at each minute
	node_time_dict = {}

    # a marker which marks if the device matches same time slots in other nodes
	found = 0
	for time_slot in range(0, mini_length):
		for num in range(0,len(device_list) - 1):
			# do not care about devices which only appear at the last node
			for target_device in device_list[num][time_slot].keys():
				if node_time_dict.get(target_device) == None:
					node_time_dict[target_device] = {}
				for compare_num in range(num + 1, len(device_list)):
					for device in device_list[compare_num][time_slot].keys():
						if device_list[num][time_slot][target_device] == device_list[compare_num][time_slot][device]:
							if device_list[num][time_slot][target_device].compare(device_list[compare_num][time_slot][device]):
								node_number = node[num]
							else:
								# print 'num:' + str(num) + "compare num:" + str(compare_num)
								node_number = node[compare_num]
							# {time_slot:node_number}
							node_time_dict[target_device][time_slot] = node_number
							found = 1
					# if no device in same time slot in other node, aka no comparison
					if found == 0:
						node_time_dict[target_device][time_slot] = node[num]
					# reset found
					found = 0

	return node_time_dict

# combine node_time_dict and get device's stopping time at each node
def combine_connection(node_time_dict):
	stop_time_dict = {}
	for target_device in node_time_dict.keys():
		stop_time_dict[target_device] = {}
		time_slot_list = node_time_dict[target_device].keys()
		time_slot_list.sort(key=int)
		# time_slot_iterator = iter(time_slot_list)
		start_time = time_slot_list[0]
		node_number = node_time_dict[target_device][start_time]
		# if next(time_slot_iterator, None) == None:
		# 	# iteration complete

		for time_slot in time_slot_list:
			#{target_device:{start_time:{node_number:time_interval}}}
			if node_time_dict[target_device][time_slot] != node_number and time_slot != time_slot_list[-1]:
				stop_time_dict[target_device][start_time] = {node_number:time_slot - start_time}
				node_number = node_time_dict[target_device][time_slot]
				start_time = time_slot

			if node_time_dict[target_device][time_slot] != node_number and time_slot == time_slot_list[-1]:
				stop_time_dict[target_device][start_time] = {node_number:time_slot - start_time}
				stop_time_dict[target_device][time_slot] = {node_time_dict[target_device][time_slot]:1}
				

			if node_time_dict[target_device][time_slot] == node_number and time_slot == time_slot_list[-1]:
				stop_time_dict[target_device][start_time] = {node_number:time_slot - start_time + 1}
		
	return stop_time_dict

# remove device which only appears at one node
def remove_single_device(stop_time_dict):
	process_dict = dict(stop_time_dict)
	count = 0
	for target_device in process_dict.keys():
		if len(process_dict[target_device]) < 2:
			count +=1
			del process_dict[target_device]
	# print count
	# print len(process_dict)
	return process_dict

