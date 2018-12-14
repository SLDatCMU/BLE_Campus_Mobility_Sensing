import sys
from device_list_time_slot import get_device_list
from sets import Set
node = [3, 12]
def connectivity_at_certain_time(time, device_list, node, connect_time):
    """
        this module is to build graph(dict) based on the device list
        Args:
            time: desired time to process
            device_list : device list read before (list of list of dict)
        Returns:
            dict : dictionary contains the graph built
    """
    dict = {}
    set = Set()
    length = len(device_list)
    for t in range(time, time + 30):
        for i in range(0, length):
            temp_dict = device_list[i]
            for key in temp_dict[t].keys():
                for j in range(0, length):
                    if (j == i):
                        continue
                    for x in range(t, time + connect_time):
                        if (key in device_list[j][x].keys()):
                            if (key in set):
                                continue
                            if (dict.get(str(node[i]) + " " + str(node[j])) == None):
                                dict[str(node[i]) + " " + str(node[j])] = 1
                            else:
                                dict[str(node[i]) + " " + str(node[j])] += 1
                            set.add(key)
                            break
    return dict

def remove_duplicate_device(device_list):
    """Remove the same device number shows at the same time in differet node
        Args:
        device_list: the device list read from files
        Return:
        device_list: removed all of the duplicate deivce at the same time
    """
    min_len = get_min_length(device_list)
    len_device_list = len(device_list)
    # from time slot 0 to the end of the day
    for t in range(0, min_len):
        #iterate all of the node
        for i in range(0, len_device_list):
            # interate from the node after i to avoid duplicate operation
            for j in range(i + 1, len_device_list):
                # check if there is duplicate device
                for key in device_list[i][t].keys():
                    if (key in device_list[j][t].keys()):
                        if (device_list[i][t][key].compare(device_list[j][t][key])):
                            del device_list[j][t][key]
                        else:
                            del device_list[i][t][key]

def time_switch(desired_time, time_slot):
    """
        this module is to switch time from Britsih time to ET
        Args:
        desired_time: time at ET
        Returns:
        the return vlue: the list position
        """
    return (desired_time + 4) * 6 * 60 / time_slot

def get_min_length(device_list):
    """Get the min time length of all of the node to avoid out of index limit error
       Args:
            device_list: the device list read in
       Returns:
            the min len of the node
    """
    min_len = len(device_list[0])
    for list in device_list:
        if min_len > len(list):
            min_len = len(list)
    return min_len

def dict_to_graph(dict):
    """
        this module is to build graph based on the dictionary
        Args:
        dict : dictionary contains the graph built
        Returns:
        G : graph we built with label (weight)
        """
    G = nx.MultiDiGraph()
    
    for key in dict.keys():
        pos = key.split(" ")
        G.add_edge(pos[0], pos[1], weight=int(dict.get(key)))
    return G


if __name__ == '__main__':
    input_date = sys.argv[1]
    time_slot = int(str(sys.argv[2]))
    desired_time = int(sys.argv[3])
    device_list = get_device_list(node, input_date, time_slot)
    remove_duplicate_device(device_list)
    dict = connectivity_at_certain_time(time_switch(desired_time, time_slot), device_list, node, 30 * 6 / time_slot)
    print dict