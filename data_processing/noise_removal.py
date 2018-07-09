from sets import Set

def get_static_dict_all_day(device_dict):
    """
        remove static some static device which always appears in the record
        Args:
            device_dict: device dictionary
        Return:
            return the static list
    """
    result = Set()
    for key in device_dict.keys():
        if (device_dict[key] > 4300):
            result.add(key)
    return result
