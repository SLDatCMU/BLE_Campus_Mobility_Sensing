#! /usr/bin/python
# Useful reference for Bluetooth and bluepy:
# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.83.1707&rep=rep1&type=pdf

import bluetooth as bt
import inquiry_with_rssi as bt_rssi 
from bluepy.btle import UUID, Scanner
import datetime
import os, sys
import time
import re
import math

# Scanning period in seconds
SCAN_PERIOD = 10.0
HEADER_STR = "ADDR\tADDRTYPE\tNAME\tDEVCLASS\tRSSI\tRFTYPE\tCONNECTABLE\n"
FORMAT_STR = "{}\t" * HEADER_STR.count("\t") + "{}\n"
ble_scanner = Scanner() #.withDelegate(ScanDelegate())
#bt_socket = bt_rssi.setup_bluetooth_inquiry()
bt_socket = None

# Based on inquiry with rssi example here:
# https://github.com/broadstone/pybluez/blob/master/examples/advanced/inquiry-with-rssi.py
def poll_bt(sock, timeout=1):
    dur = int(math.ceil(timeout/1.28))
    bt_devices = bt.discover_devices(duration=dur, lookup_names=True)
    #bt_devices = bt_rssi.device_inquiry_with_rssi(sock, duration=dur)
    return bt_devices 

def poll_ble(ble_scanner, timeout=1):
    ble_devices = ble_scanner.scan(SCAN_PERIOD)
    return ble_devices

def poll_wifi(timeout=1):
    pass

def log_to_file(fname, prev_date):
    global bt_socket, ble_scanner
    global HEADER_STR, FORMAT_STR
    fh = open(fname, "w")
    fh.write(HEADER_STR)
    while True:
        # Check  that we are on the same day as the file handle we are writing to:
        new_date = datetime.datetime.utcnow()
        if new_date.date() != prev_date.date():
            prev_date = new_date
            fh.close()
            break

        current = datetime.datetime.utcnow()
        current_hour = current.hour
        bt_devices = poll_bt(bt_socket, timeout=SCAN_PERIOD)
        ble_devices = poll_ble(ble_scanner, timeout=SCAN_PERIOD)

        for addr, name in bt_devices:
            fh.write(FORMAT_STR.format(addr, '', name, '', '', 'bt', ''));
        for dev in ble_devices:
            name = ""
            for (adtype, desc, value) in dev.getScanData():
                #if dev.addrType == "public":
                #    print("{} {}".format(dev.addr, dev.addrType))
                #    print("{} {} {}".format(adtype, desc, value))
                #    print("\n")
                if "name" in desc.lower():
                    name = value
            fh.write(FORMAT_STR.format(dev.addr, dev.addrType, name, '', dev.rssi, 'ble', dev.connectable))
        fh.flush()

    return prev_date

def next_fname(node_num, prev_date):
    date_str = str(prev_date.date())
    # Find next available data file handle:
    i = 0
    while os.path.exists(DATA_PATH+"n%s_%s_%s.txt" % (node_num, date_str,i)):
        i += 1
    return str(DATA_PATH+"n%s_%s_%s.txt" % (node_num, date_str ,i))


######################################################################################


if __name__ == "__main__":
    # Get hostname and node number from hostname:
    with open('/etc/hostname', 'r') as fh:
        hostname = fh.readline().strip()
    try:
        node_num = int(re.findall( r'\d+', hostname )[0])
        DATA_PATH = "/home/pi/BLE_Campus_Mobility_Sensing/passive_ble/data/".lower()
    except:
        if hostname == "TacitMonolith":
            DATA_PATH = "/home/mark/Documents/Repos/BLE_Campus_Mobility_Sensing/passive_ble/data/"
            node_num = 0
        else:
            print "Cannot get node number from hostname. Is hostname correctly set?"
            sys.exit(1)
   
    prev_date = datetime.datetime.utcnow()
    # Log for all time!
    while True:
        fname = next_fname(node_num, prev_date)
        prev_date = log_to_file(fname, prev_date)
