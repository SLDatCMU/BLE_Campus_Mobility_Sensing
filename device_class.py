# -*- coding: utf-8 -*-
from sets import Set
"""
    Device Class
"""
class Device:
    # device address
    device = ""
    #when device shows up
    no = 0
    # mean value of the rssi value shows up in same time slot
    rssi_mean = 0
    # deviec count in same time slot
    count = 0

    def __init__(self, device_name, device_no, rssi):
        """Device Class Constructor
        
        Args:
            self:
            device_name: the device address of a device
        """
        self.device = device_name
        self.no = device_no
        self.rssi_mean = rssi
        self.count = 1

    def add(self, rssi):
        """Add a device to existing device
            Args:
                rssi: the rssi value of device
                no_new: when the device shows up
        """
        self.count += 1
        self.rssi_mean = float(self.rssi_mean * (self.count - 1) + rssi) / float(self.count)

    def compare(self, device_to_compare):
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

    def __eq__(self, device_to_compare):
        """Check is self device is same as input device
            Returns:
                True: same
                False: different
        """
        if (self.device == device_to_compare.device):
            return True
        return False

    def __hash__(self):
        """Hash function based on the device address
           Argvs:
                self
           Returns:
                hash code
        """
        return hash(self.device)

    def __str__(self):
        """To String Method
            Args:
                self
                Returns: the string of this class
        """
        return self.device + " No: " + str(self.no) + " rssi: " + str(self.rssi_mean)



