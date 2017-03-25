import time
import Adafruit_PCA9685

LEFT_POINT = 490
RIGHT_POINT = 250 
BOTTOM_POINT = 450
TOP_POINT = 300 

PAN_CHANNEL = 0
TILT_CHANNEL = 7

class PanTiltManager:
  
  def __init__(self):
     self.pwm = Adafruit_PCA9685.PCA9685()
     self.pwm.set_pwm_freq(60)  # freq set to 60hz for servos

     self.panMidPoint = int(RIGHT_POINT + (LEFT_POINT - RIGHT_POINT) / 2)     
     self.tiltMidPoint = int(TOP_POINT + (BOTTOM_POINT - TOP_POINT) / 2)
     self.panTo(self.panMidPoint)
     self.tiltTo(self.tiltMidPoint)

  def panTo(self, point):
     point = max(min(point, LEFT_POINT), RIGHT_POINT)
     self.pwm.set_pwm(PAN_CHANNEL, 0, point)
     self.panPosition = point
  
  def getPanPosition(self):
     return self.panPosition

  def tiltTo(self, point):
     point = max(min(point, BOTTOM_POINT), TOP_POINT)
     self.pwm.set_pwm(TILT_CHANNEL, 0, point)
     self.tiltPosition = point

  def getTiltPosition(self):
     return self.tiltPosition
