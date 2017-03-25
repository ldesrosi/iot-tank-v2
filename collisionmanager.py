#!/usr/bin/python

import smbus
import time

BUS_ID = 1
DEVICE_ADDRESS = 0x04

class CollisionManager: 

  def __init__(self):
    self.bus = smbus.SMBus(BUS_ID)
    self.address = DEVICE_ADDRESS
    self.leftSensor = False
    self.rightSensor = False
    self.distance = 0
    self.lastUpdate = -1

  def getCollisionData(self):
    colData = bytearray()
    colData = self.bus.read_i2c_block_data(self.address,2)
 
    self.leftSensor = (colData[0]&1 != 0)
    self.rightSensor = (colData[0]&1 != 0)
    self.distance = colData[1]
    self.lastUpdate = time.time()

