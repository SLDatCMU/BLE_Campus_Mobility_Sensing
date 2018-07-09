""" Data Analysis based on Graph
    This code will generate grapg.out file to print out our desired graph
    author: Zhengkai Zhang
"""
import sys
import numpy as np
import networkx as nx
import pylab as plt
from sets import Set
from networkx.drawing.nx_agraph import write_dot

def get_static_device(file_name, time_from, time_to):
    """
        this module is to get static devices during mid night to remove
        data noise to produce cleaner data.
        Args:
            file_name: input file to read from disk
            time_from: the time when static device name record starts
            time_to: the time when static device record ends
        Returns:
            static_device: the static device list
    """
    with open(file_name) as f:
        while (True):
            line = f.readline().split(" ");
            if (len(line) < 3):
                continue
            if (line[0] == '*') & ((line[2].split(':')[0] == time_from)):
                break
        static_device = Set();
        while (True):
            line = f.readline().split(" ");
            if (line[0] == '*'):
                if (line[2].split(':')[0] == time_to):
                    break
                else:
                    continue
            static_device.add(line[0])
    return static_device

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

def connectivity_at_certain_time(time, device_list):
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
                        if (dict.get(str(i) + " " + str(j)) == None):
                            dict[str(i) + " " + str(j)] = 1
                        else:
                            dict[str(i) + " " + str(j)] += 1
    return dict

def dictToGraph(dict):
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

def main():
    # set static device record time from
    time_from = '02';
    # set static device record time to
    time_to = '06';

    static_device = []
    device_list = []
    for i in range(1, 10):
        file_name = sys.argv[i]
        static_device.append(get_static_device(file_name, time_from, time_to));
        device_list.append(read_device(file_name, static_device[i - 1]));
    dict = connectivity_at_certain_time(time_switch(18), device_list);
    G = dictToGraph(dict)
    #write out to .dot file
    write_dot(G, 'graph.dot')

if __name__ == '__main__':
    main()


