#!/usr/bin/python
import threading
import smbus
import time

BUS_ID = 1
DEVICE_ADDRESS = 0x04

class CollisionSensor(threading.Thread):

  def __init__(self, dataRecorder=None):
    threading.Thread.__init__(self)
    self.done = False
    self.dataRecorder = dataRecorder
    self.bus = smbus.SMBus(BUS_ID)
    self.address = DEVICE_ADDRESS
    self.leftSensor = False
    self.rightSensor = False
    self.distance = 0
    self.lastUpdate = -1
    self.listeners = []

  def addEventListener(self, listener):
      if not (listener is None):
          listeners.append(listener)

  def stop(self):
    self.done = True

  def run(self):
    print("[collision: starting collision monitoring]")
    while (not self.done):
      self.getCollisionData()
      self.dataRecorder.record([{"left_ir":int(self.leftSensor)},{"right_ir":int(self.rightSensor)},{"distance":int(self.distance)}])
      # Wait half a second before repeating
      if (self.leftSensor or self.rightSensor):
          event = {'leftSensor':self.leftSensor, 'rightSensor':self.rightSensor, 'distance':self.distance}
          for listener in listeners:
              listener(event)
          
      time.sleep(0.5)
    print("[collision: shutting down collision monitoring]")

  def getCollisionData(self):
    colData = bytearray()
    colData = self.bus.read_i2c_block_data(self.address,2)

    self.leftSensor = (colData[0]&1 != 0)
    self.rightSensor = (colData[0]&1 != 0)
    self.distance = colData[1]
    self.lastUpdate = time.time()
