""" Data Analysis based on Graph
    This code will generate grapg.out file to print out our desired graph
"""
import sys
import networkx as nx
import pylab as plt
from sets import Set

def read_device(file_name, static_device):
    """
        this module is to read the device list from disk and remove noise.
        Args:
            file_name: input file to read from disk
            static_device: the static device list
        Returns:
            device_list: a list of set which store data from each node after
                        removing noise
    """
    device_list = [];
    block = -1;
    with open(file_name) as f:
        for line in f.readlines():
            list = line.split(" ")
            if (list[0] == '*'):
                block += 1
                device_list.append(Set())
                continue
            else:
                if (list[0] in static_device):
                    continue
                device_list[block].add(list[0])

    return device_list

def time_switch(desired_time):
    """
        this module is to switch time from BST to ET
        Args:
            desired_time: time at ET
        Returns:
            the return vlue: the list position
    """
    return (desired_time + 4) * 6 * 60

def connectivity_at_certain_time(time, device_list, node):
    """
        this module is to build graph based on the device list
        Args:
            time: desired time to process
            device_list : device list read befor
        Returns:
            dict : dictionary contains the graph built
    """
    device_count = len(device_list)
    dict = {}
    length = len(device_list);
    for i in range(0, length):
        temp_set = device_list[i]
        for entry in temp_set[time]:
            for j in range(0, length):
                if (j == i):
                    continue
                for x in range (1, 6):
                    if (entry in device_list[j][time + x]):
                        if (dict.get(str(node[i]) + " " + str(node[j])) == None):
                            dict[str(node[i]) + " " + str(node[j])] = 1
                        else:
                            dict[str(node[i]) + " " + str(node[j])] += 1
    return dict

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
        G.add_edge(pos[0], pos[1], label=str(dict.get(key)))
    return G

