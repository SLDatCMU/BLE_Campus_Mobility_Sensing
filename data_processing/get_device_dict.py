def device_to_dict(node):
    """
        Read from data files to generate device dictionary for one node
        Args:
            node: input node number list
        Return:
            Device list
    """
    device_dict = []
    num = 0;
    for n in node:
        file_name = 'n' + str(n) + '_2018-06-28_0.txt'
        device_dict.append({})
        with open(file_name) as f:
            for line in f.readlines():
                list = line.split(" ")
                if (list[0] == '*'):
                    continue
                else:
                    if (device_dict[num].get(list[0]) == None):
                        device_dict[num][list[0]] = 1
                    else:
                        device_dict[num][list[0]] += 1
        num += 1
    return device_dict


