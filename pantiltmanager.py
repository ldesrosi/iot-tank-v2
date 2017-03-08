from __future__ import division
import time
import Adafruit_PCA9685

LEFT_POINT = 450
RIGHT_POINT = 250 
BOTTOM_POINT = 450
TOP_POINT = 300 

PAN_CHANNEL = 0
TILT_CHANNEL = 7

class PanTiltManager:
  
  def __init(self)__:
     self.pwm = Adafruit_PCA9685.PCA9685()
     self.set_pwm_freq(60)    # frequency set to 60hz, appropriate for servos.
     
     self.panTo(RIGHT_POINT + (LEFT_POINT - RIGHT_POINT) / 2)
     self.tiltTo(TOP_POINT + (BOTTOM_POINT - TOP_POINT) / 2)

   def panTo(self, point):
     point = max(min(point, LEFT_POINT), RIGHT_POINT)
     self.pwm.set_pwm(PAN_CHANNEL, 0, point)
     self.panPosition = point

   def tiltTo(self, point):
     point = max(min(point, TOP_POINT), BOTTOM_POINT)
     self.pwm.set_pwm(TILT_CHANNEL, 0, point)
     self.tiltPosition = point

