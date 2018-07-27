import sys
from device_list_time_slot import get_device_list
import networkx as nx
from sets import Set

node = [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,18,20,21,22,23]
def connectivity_at_certain_time(time, device_list, node, connect_time):
    time = int(time)
    """
        this module is to build graph(dict) based on the device list
        Args:
            time: desired time to process
            device_list : device list read before (list of list of dict)
        Returns:
            dict : dictionary contains the graph built
    """
    dict = {}
    length = len(device_list)
    nnset = Set()
    for t in range(time, time + connect_time):
        for i in range(0, length):
            temp_dict = device_list[i]
            for key in temp_dict[t].keys():
                set = Set()
                for x in range(t, time + connect_time):
                    for j in range(0, length):
                        if (j == i):
                            continue
                        if (key in device_list[j][x].keys()):
                            # at one time
                            if (key in set):
                                continue
                            # one device can only have connectivity between two nodes
                            if (key + str(node[i]) + str(node[j])) in nnset:
                                continue
                            if (dict.get(str(node[i]) + " " + str(node[j])) == None):
                                nnset.add(key + str(node[i]) + str(node[j]))
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
    return float(desired_time + 4) * 6.0 * 60.0 / time_slot

def get_min_length(device_list):
    """Get the min time length of all of the node to avoid out of index limit error
       Args:
            device_list: the device list read in
       Returns:
            the min len of the node
    """
    min_len = len(device_list[0])
    for list in device_list:
        print len(list)
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
    node = get_node_attributes(dict)
    for n in node.keys():
        G.add_node(n, attri=float(node.get(n)))

    for key in dict.keys():
        pos = key.split(" ")
        G.add_edge(pos[0], pos[1], weight=float(dict.get(key)))
    return G

def get_node_attributes(dict):
    """
        Add attributes to node indegree - outdegree
        Args:
            dict: input dict based graph
        Return:
            node dict
    """
    node = {}
    min = sys.maxint
    for key in dict.keys():
        pos = key.split(" ")
        for i in range(0, 2):
            if i == 1:
                t = 1
            if i == 0:
                t = -1
            if pos[i] in node:
                node[pos[i]] += t * float(dict.get(key))
            else:
                node[pos[i]] = t * float(dict.get(key))
    return node

def node_list_to_csv(node_list, input_date, path):
    """
        Write the node list to Gephi csv format dynamic graph
        Args:
            node_list: input node_list which is a list of dict which contains the
                       attributes of each at certain time
            input_date: the date of the data processing
            path: where the csv files stores
        Return:
    """
    id, time_stamp, attributes = graph_to_csv_formter(node_list);
    
    loc = path + '/graph/'
    f = open(loc + input_date + '_node.csv', 'w')
    f.write('Id,Label,timeset,Population\n')
    for key in id.keys():
        f.write(str(key) + ',' + str(key) + ',"<[')
        length = len(time_stamp[id[key]])
        # write time stamp set
        for i in range(0, length - 1):
            f.write(str(time_stamp[id[key]][i]) + ', ')
        f.write(str(time_stamp[id[key]][length - 1]))
        f.write(']>","<')
        # write node attributes set
        for i in range(0, length - 1):
            f.write('[')
            f.write(str(time_stamp[id[key]][i]))
            f.write(', ')
            f.write(str(attributes[id[key]][i]))
            f.write(']; ')
        f.write('[')
        f.write(str(time_stamp[id[key]][length - 1]))
        f.write(', ')
        f.write(str(attributes[id[key]][length - 1]))
        f.write(']>"\n')
    f.close()

def edge_list_to_csv(edge_list, input_date, path):
    """
        Write the node list to Gephi csv format dynamic graph
        Args:
            edge_list: input node_list which is a list of dict which contains the
                       weight(Connectivity) of each at certain time
            input_date: the date of the data processing
            path: where the csv files stores
        Return:
        """
    edge, time_stamp, weight = graph_to_csv_formter(edge_list);

    loc = path + '/graph/'
    f = open(loc + input_date + '_edge.csv', 'w')
    f.write('Source,Target,Type,Id,Label,timeset,Connectivity\n')
    temp = 0
    for key in edge.keys():
        list = key.split(" ");
        f.write(list[0] + ',' + list[1] + ',' + 'Directed' + ',' + str(temp) + ',' +',"<[')
        temp += 1
        length = len(time_stamp[edge[key]])
        for i in range(0, length - 1):
            f.write(str(time_stamp[edge[key]][i]) + ', ')
        f.write(str(time_stamp[edge[key]][length - 1]))
        f.write(']>","<')
        for i in range(0, length - 1):
            f.write('[')
            f.write(str(time_stamp[edge[key]][i]))
            f.write(', ')
            f.write(str(weight[edge[key]][i]))
            f.write(']; ')
        f.write('[')
        f.write(str(time_stamp[edge[key]][length - 1]))
        f.write(', ')
        f.write(str(weight[edge[key]][length - 1]))
        f.write(']>"\n')
    f.close()

def graph_to_csv_formter(input_list):
    """
        Format the graph into Gephi csv files
    """
    id = {}
    time_stamp = []
    attributes = []
    time = 1.0
    count = 0
    for list in input_list:
        for key in list.keys():
            if (key in id):
                time_stamp[id[key]].append(time)
                attributes[id[key]].append(list[key])
            else:
                id[key] = count
                time_stamp.append([])
                attributes.append([])
                time_stamp[count].append(time)
                attributes[count].append(list[key])
                count += 1
        time += 1.0

    return id, time_stamp, attributes

def main():
    input_date = sys.argv[1]
    time_slot = int(sys.argv[2])
    path = sys.argv[3]
    connect_time = 15
    device_list = get_device_list(node, input_date, time_slot, path)
    remove_duplicate_device(device_list)
    edge_list = []
    node_list = []
    for i in range(6, 19):
        for j in range (0, 4):
            desired_time = i + j * 0.25
            dict = connectivity_at_certain_time(time_switch(desired_time, time_slot), device_list, node, connect_time * 6 / time_slot)
            node_list.append(get_node_attributes(dict))
            edge_list.append(dict)
    connectivity_analysis(edge_list)
    node_list_to_csv(node_list, input_date, path)
    edge_list_to_csv(edge_list, input_date, path)

if __name__ == '__main__':
    main()
