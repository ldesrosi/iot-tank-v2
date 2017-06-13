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

      self.dataRecorder = dataRecorder

   def block(self):
       self.blocked = True
       self.stop()

   def unblock(self):
       self.blocked = False

   def forward(self, speed):
       if not self.blocked:
          speed = max(min(speed, 1), 0)
          self.motor_fl.forward(speed)
          self.motor_fr.forward(speed)
          self.motor_bl.forward(speed)
          self.motor_br.forward(speed)
          self.dataRecorder.record([{"FL":float(speed)},{"FR":float(speed)},{"BL":float(speed)},{"BR":float(speed)}])

   def backward(self, speed):
       if not self.blocked:
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

   def right(self, speed):
       if not self.blocked:
          self.motor_fl.forward(speed)
          self.motor_bl.forward(speed)
          self.motor_fr.backward(speed)
          self.motor_fr.backward(speed)
          self.dataRecorder.record([{"FL":float(speed)},{"FR":float(-speed)},{"BL":float(speed)},{"BR":float(-speed)}])

   def left(self, speed):
       if not self.blocked:
          self.motor_fl.backward(speed)
          self.motor_bl.backward(speed)
          self.motor_fr.forward(speed)
          self.motor_fr.forward(speed)
          self.dataRecorder.record([{"FL":float(-speed)},{"FR":float(speed)},{"BL":float(-speed)},{"BR":float(speed)}])
