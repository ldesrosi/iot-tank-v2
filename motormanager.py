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

   def __init__(self, max_rpm, wheel_diameter):
      self.motor_br = Motor(27, 24)
      self.motor_br_enable = OutputDevice(5, initial_value=1)
      self.motor_bl = Motor(22, 6)
      self.motor_bl_enable = OutputDevice(17, initial_value=1)
      self.motor_fr = Motor(23, 16)
      self.motor_fr_enable = OutputDevice(12, initial_value=1)
      self.motor_fl = Motor(18, 13)
      self.motor_fl_enable = OutputDevice(25, initial_value=1)
      self.max_rpm = max_rpm
      self.wheel_diameter = wheel_diameter
      self.dist_per_turn = math.pi * wheel_diameter

   def calculateTurnDuration(self, rpm, angle):
      return 3

   def forward(self, speed):
      speed = max(min(speed, 1), 0)
      self.motor_fl.forward(speed) 
      self.motor_fr.forward(speed) 
      self.motor_bl.forward(speed)
      self.motor_br.forward(speed)

   def backward(self, speed):
      speed = max(min(speed, 1), 0)
      self.motor_fl.backward(speed)
      self.motor_fr.backward(speed)
      self.motor_bl.backward(speed)
      self.motor_br.backward(speed)

   def stop(self): 
      self.motor_fl.stop() # stop the motor
      self.motor_fr.stop() # stop the motor
      self.motor_bl.stop() # stop the motor
      self.motor_br.stop() # stop the motor

   def right(self, speed, angle, callback):
      speed = max(min(speed, 1), 0)
      angle = max(min(angle, 360), 0)
      duration = self.calculateTurnDuration(self.max_rpm * speed, angle)

      self.motor_fl.forward(speed)
      self.motor_bl.forward(speed)
      self.motor_fr.backward(speed)
      self.motor_fr.backward(speed)
      
      sleep(duration)

      callback(speed)

   def left(self, speed, angle, callback):
      speed = max(min(speed, 1), 0)
      angle = max(min(angle, 360), 0)
      duration = self.calculateTurnDuration(self.max_rpm * speed, angle)

      self.motor_fl.backward(speed)
      self.motor_bl.backward(speed)
      self.motor_fr.forward(speed)
      self.motor_fr.forward(speed)

      sleep(duration)

      callback(speed)
