import sys
from get_device_dict import device_to_dict
from noise_removal import get_static_dict_all_day
from graph_helper import read_device, connectivity_at_certain_time, time_switch, dict_to_graph
from networkx.drawing.nx_agraph import write_dot

node = [3,4,5,6,7,9,10,11,12]

def read_device_without_noise(static_device_set):
    device_list = []
    i = -1
    for n in node:
        i += 1
        file_name = 'n' + str(n) + '_2018-06-28_0.txt'
        device_list.append(read_device(file_name, static_device_set[i]))
    return device_list


def get_static_devic_set(device_dict):
    static_device_set = []
    for i in range(0, len(node)):
        static_device_set.append(remove_static_list_all_day(device_dict[i]))
    return static_device_set


def main():
    device_dict = device_to_dict(node)
    static_device_set = get_static_devic_set(device_dict)
    device_list = read_device_without_noise(static_device_set)
    dict = connectivity_at_certain_time(time_switch(int(sys.argv[1])), device_list, node);
    G = dict_to_graph(dict)
    write_dot(G, 'graph.dot')


if __name__ == '__main__':
    main()
