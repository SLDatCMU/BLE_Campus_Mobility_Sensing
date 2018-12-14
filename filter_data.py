import sys
import networkx as nx
import pylab as plt
from sets import Set
from get_device_dict import get_device_dict
from noise_removal import get_static_set
import os.path

# node = [3, 12]

# node = [i for i in range(1,27) if i not in [9,11,15,17,21,23]]
node = [i for i in range(1,29) if i not in [2, 11, 17]]
# node = [i for i in range(1,29) if i not in [1,10,19,22,24,27,11,17]]

# keep a record of except nodes with regard to dates(11,17 default)
# 2018-10-04: 2
# 2018-10-03: 8
# 2018-10-02: 8
# 2018-10-01: 4



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
    if n < 10:
        fname = 'data_collection/node0' + str(n) + '/data/' + 'n' + str(n) + '_' + date + '_r.txt'
        if os.path.isfile(fname):
            file_name = fname
        else:
            file_name = 'data_collection/node0' + str(n) + '/data/' + 'n' + str(n) + '_' + date + '_0.txt'
    else:
        fname = 'data_collection/node' + str(n) + '/data/' + 'n' + str(n) + '_' + date + '_r.txt'
        if os.path.isfile(fname):
            file_name = fname
        else:
            file_name = 'data_collection/node' + str(n) + '/data/' + 'n' + str(n) + '_' + date + '_0.txt'
    device_dict = get_device_dict(file_name)
    static_device = get_static_set(device_dict)
    write_clean_device(file_name, static_device, n, date)

def data_filter(node, date):
    for n in node:
        data_filter_helper(n, date)

if __name__ == '__main__':
    date = sys.argv[1]
    data_filter(node, date)


