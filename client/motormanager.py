from gpiozero import Motor, OutputDevice
from time import sleep
import math

# Motor nomenclature
#      Front
# L 0-(fl) (fr)-0 R
# E               I
# F               G
# T 0-(bl) (br)-0 H
#                 T
#       Back

class MotorManager:

   def __init__(self, dataRecorder=None):
      self.motor_br = Motor(27, 24)
      self.motor_br_enable = OutputDevice(5, initial_value=1)
      self.motor_bl = Motor(22, 6)
      self.motor_bl_enable = OutputDevice(17, initial_value=1)
      self.motor_fr = Motor(23, 16)
      self.motor_fr_enable = OutputDevice(12, initial_value=1)
      self.motor_fl = Motor(18, 13)
      self.motor_fl_enable = OutputDevice(25, initial_value=1)

      self.blocked = False
      self.block_id = None

      self.dataRecorder = dataRecorder
      self.lock = threading.Lock()

   def block(self, block_id):
       with lock:
           if verifyBlock(block_id):
               self.block_id = block_id
               self.stop()

   def unblock(self, block_id):
       with lock:
           if verifyBlock(block_id):
               self.block_id = None

   def verifyBlock(self, block_id):
       if (self.block_id is None):        #No block set... ok to proceed
           return True
       elif (block_id is None):           #Block set but function called without block id... block the call
           return False
       elif (self.block_id == block_id):  #Block set and function received a matching block... allow the call
           return True
       else:
           raise ValueError('Wrong block_id received.  Expected ' + str(self.block_id) + '. Received ' + str(block_id))

   def forward(self, speed, block_id=None):
       if self.verifyBlock:(block_id):
          speed = max(min(speed, 1), 0)
          self.motor_fl.forward(speed)
          self.motor_fr.forward(speed)
          self.motor_bl.forward(speed)
          self.motor_br.forward(speed)
          self.dataRecorder.record([{"FL":float(speed)},{"FR":float(speed)},{"BL":float(speed)},{"BR":float(speed)}])

   def backward(self, speed, block_id=None):
       if self.verifyBlock:(block_id):
          speed = max(min(speed, 1), 0)
          self.motor_fl.backward(speed)
          self.motor_fr.backward(speed)
          self.motor_bl.backward(speed)
          self.motor_br.backward(speed)
          self.dataRecorder.record([{"FL":float(-speed)},{"FR":float(-speed)},{"BL":float(-speed)},{"BR":float(-speed)}])

   def stop(self):
      self.motor_fl.stop() # stop the motor
      self.motor_fr.stop() # stop the motor
      self.motor_bl.stop() # stop the motor
      self.motor_br.stop() # stop the motor
      self.dataRecorder.record([{"FL":0.0},{"FR":0.0},{"BL":0.0},{"BR":0.0}])

   def right(self, speed, block_id=None):
       if self.verifyBlock:(block_id):
          self.motor_fl.forward(speed)
          self.motor_bl.forward(speed)
          self.motor_fr.backward(speed)
          self.motor_fr.backward(speed)
          self.dataRecorder.record([{"FL":float(speed)},{"FR":float(-speed)},{"BL":float(speed)},{"BR":float(-speed)}])

   def left(self, speed, block_id=None):
       if self.verifyBlock:(block_id):
          self.motor_fl.backward(speed)
          self.motor_bl.backward(speed)
          self.motor_fr.forward(speed)
          self.motor_fr.forward(speed)
          self.dataRecorder.record([{"FL":float(-speed)},{"FR":float(speed)},{"BL":float(-speed)},{"BR":float(speed)}])
