#!/usr/bin/python

import smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

colData = bytearray()

while True:
  colData = bus.read_i2c_block_data(address,2)
  
  print "State: ", colData[0]
  print

  print "Distance: ", colData[1]
  print

  # sleep one second
  time.sleep(1)
