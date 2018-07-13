#!/usr/bin/python
# Adapted from here: https://www.raspberrypi.org/forums/viewtopic.php?t=108112

import spidev
import string
import time
import os
from time import gmtime, strftime

# Definitions
channel_0        = 0               # ADC Channel 0
channel_1        = 1               # ADC Channel 1
delay            = 5               # Delay between readings
measurements     = 5               # Number of readings for average value

# Be sure to measure this on the actual system and set it accordingly!
VREF = 5.0

# Open SPI bus
spi              = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

# Function to read SPI data from MCP3002 chip
# Channel must be an integer 0|1
def ReadChannel(channel, MSB=True):
  data           = 0
  acc = 0.0
  for i in range(0,measurements):
    cmd = 0x18 | ( channel << 2 ) | ( int(MSB) << 1)
    adc         = spi.xfer2([cmd, 0x00, 0x00, 0x00])
    if MSB:
        msb_data = int( (adc[1] << 2) + ((adc[2] & 0xc0) >> 6) )   
        tmp = int( ( (adc[2] & 0x7f) << 3) + ( ( adc[3] & 0xe0 ) >> 5 ) )
        lsb_data = int("{:010b}".format(tmp)[::-1], 2)
        print("{:010b} {:010b}".format(msb_data, lsb_data))
        if lsb_data != msb_data:
            raise Exception("MSB and LSB formatted data did not match!")
        else:
            data = msb_data
    else:
        # data came in lsb formatted, only.
        tmp = int( (adc[1] << 2) + ( ( adc[2] & 0xc0 ) >> 6) )
        # for some reason the data does not need to be reversed in this case??
        data =  tmp

    print(data)
    time.sleep(0.2)
    print("{:08b} {:08b} {:08b} {:08b}".format(adc[0], adc[1], adc[2], adc[3]))
    acc += float(data)
  data           = float(acc) / measurements
  return data

while True:
  level = ReadChannel(channel_1)
  volts = round((level * VREF) / float(1024), 2)

  # Print out results
  timenow = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
  print("time: {} | {} steps | {} volts".format(timenow, level, volts))

  # Wait before repeating loop
  time.sleep(delay)
