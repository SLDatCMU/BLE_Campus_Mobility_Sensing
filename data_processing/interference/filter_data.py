import sys
import networkx as nx
import pylab as plt
from sets import Set
from get_device_dict import get_device_dict
from noise_removal import get_static_set

node = [3, 12]

"""This File is to filter out the static device shows in all of the node
"""

def write_clean_device(file_name, static_device, n, date):
    fOutput = open('n' + str(n) + '_' + date + '_c.txt', 'w')
    block = -1;
    with open(file_name) as f:
        for line in f.readlines():
            list = line.split(" ")
            if (list[0] == '*'):
                fOutput.write(line)
                block += 1
                continue
            else:
                if (list[0] in static_device):
                    continue
                fOutput.write(line)
        fOutput.close()

def data_filter_helper(n, date):
    file_name = 'n' + str(n) + '_' + date + '_0.txt'
    device_dict = get_device_dict(file_name)
    static_device = get_static_set(device_dict)
    write_clean_device(file_name, static_device, n, date)

def data_filter(node, date):
    for n in node:
        data_filter_helper(n, date)

if __name__ == '__main__':
    date = sys.argv[1]
    data_filter(node, date)


