def device_to_dict(file_name):
    """
        Read from data files to generate device dictionary for one node
        Args:
            node: input node number list
        Return:
            Device list
    """
    device_dict = {}
    with open(file_name) as f:
        for line in f.readlines():
            list = line.split(" ")
            if (list[0] == '*'):
                continue
            else:
                if (device_dict.get(list[0]) == None):
                    device_dict[list[0]] = 1
                else:
                    device_dict[list[0]] += 1
    return device_dict


