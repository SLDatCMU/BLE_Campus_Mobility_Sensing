import sys
from sets import Set
from device_class import Device

def get_device_list(node, input_date, time_slot, path):

    device_list = []
    for node_num in node:
        file_name = path + '/n' + str(node_num) + '_' + input_date + '_c.txt'
        device_list.append(get_device_single_node(file_name, time_slot))
    return device_list

def get_device_single_node(file_name, time_slot):
    count = 0
    single_device = []
    single_device.append({})
    block = 0
    with open(file_name) as f:
        for line in f.readlines():
            list = line.split(' ');
            if count == time_slot:
                count = 0
                block += 1
                single_device.append({})
            if list[0] == '*':
                count += 1
                continue
            else:
                if list[0] not in single_device[block].keys():
                    single_device[block][list[0]] = Device(list[0], count, int(list[1]))
                else:
                    single_device[block][list[0]].add(int(list[1]))
    return single_device
