# -*- coding: utf-8 -*-
"""
    Device Class
"""
class Device:

    device = ""
    no = 7
    rssi_mean = 0
    count = 0

    def __init__(self, device_name):
        """Device Class Constructor
        
        Args:
            self:
            device_name: the device address of a device
        """
        self.device = device_name

    def add_device(self, rssi, no_new):
        """Add a device to existing device
            Args:
                rssi: the rssi value of device
                no_new: when the device shows up
        """
        self.count += 1
        self.rssi_mean = float(self.rssi_mean * (self.count - 1) + rssi) / float(self.count)

        if (self.no < no_new):
            return
        else:
            self.no = no_new

    def compare_same_time(self, device_to_compare):
        """Compare two device to determine which node the device is close to
            Args:
                device_to_compare: Some device may show up at different place but at same time
            Returns:
                True: choose Self
                False: choose input device
        """
            
        if (self.rssi_mean > device_to_compare.rssi_mean + 2):
            return True
        if (self.no < device_to_compare.no):
            return True
        elif (self.no == device_to_compare.no):
            if (self.rssi_mean > device_to_compare.rssi_mean):
                return True
        return False

    def equal(self, device_to_compare):
        """Check is self device is same as input device
            Returns:
                True: same
                False: different
        """
        if (self.device == device_to_compare.device):
            return True
        return False

