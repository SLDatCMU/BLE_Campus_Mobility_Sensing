#! /usr/bin/python

# Based off of code from CMUBility for 18-651 by Tyler Goulding and Fatema Almeshquab, 2018.
# Original Repo: https://github.com/tylerGoulding/CMUbility 

from bluepy.btle import Scanner, DefaultDelegate
import datetime
import os, sys
import time
import re

# Scanning period in seconds
SCAN_PERIOD = 10.0

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

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

scanner = Scanner().withDelegate(ScanDelegate())

prev_date = datetime.datetime.utcnow()

while True:
    date_str = str(prev_date.date())
    # Find next available data file handle:
    i = 0
    while os.path.exists(DATA_PATH+"n%s_%s_%s.txt" % (node_num, date_str,i)):
        i += 1
    # Log to file for the rest of the day:
    with open(DATA_PATH+"n%s_%s_%s.txt" % (node_num, date_str ,i), "w") as fh:
        while True:
            # Check that we are on the same day as the file handle we are writing to:
            new_date = datetime.datetime.utcnow()
            if new_date.date() != prev_date.date():
                prev_date = new_date
                break

            # Otherwise scan and log devices every ten seconds:
            devices = scanner.scan(SCAN_PERIOD)
            current = datetime.datetime.utcnow()
            current_hour = current.hour
            fh.write("* " + str(current) + " " + str(len(devices)) + "\n")
            for dev in devices:
                fh.write(str(dev.addr) + " " + str(dev.rssi) + "\n");
                fh.flush()
