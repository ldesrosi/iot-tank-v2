#!/usr/bin/python

import time
import Adafruit_PWMServoDriver as driver

SERVOMIN  = 150 # this is the 'minimum' pulse length count (out of 4096)
SERVOMAX  = 600 # this is the 'maximum' pulse length count (out of 4096)

servonum = 0

# you can use this function if you'd like to set the pulse length in seconds
# e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
def setServoPulse(n, pulse):
    pulselength = 1000000.0   # 1,000,000 us per second
    pulselength /= 60.0       # 60 Hz
    print(pulselength)
    println(" us per period")
    pulselength /= 4096.0    # 12 bits of resolution
    print(pulselength)
    println(" us per bit")
    pulse *= 1000.0
    pulse /= pulselength
    print(pulse)
    pwm.setPWM(n, 0, pulse)

def setup():
    pwm = driver.PWMServoDriver()
    pwm.setPWMFreq(60) # Analog servos run at ~60 Hz updates

def loop():
    # Drive each servo one at a time
    print(servonum)
    for pulselen in range(SERVOMIN, SERVOMAX):
        pwm.setPWM(servonum, 0, pulselen)

    time.sleep(500.0/1000.0)

    for pulselen in range(SERVOMAX, SERVOMIN):
        pwm.setPWM(servonum, 0, pulselen);

    time.sleep(500.0/1000.0)

    servonum++
    if (servonum > 7):
        servonum = 0

setup()
while True:
    loop()
