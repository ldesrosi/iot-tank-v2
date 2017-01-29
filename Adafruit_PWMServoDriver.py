#!/usr/bin/python

import time
import smbus

ENABLE_DEBUG_OUTPUT = True

DEVICE_BUS = 1
DEVICE_ADDRESS = 0x40      #7 bit address (will be left shifted to add the read write bit)

PCA9685_SUBADR1 = 0x2
PCA9685_SUBADR2 = 0x3
PCA9685_SUBADR3 = 0x4

PCA9685_MODE1 = 0x0
PCA9685_PRESCALE = 0xFE

LED0_ON_L= 0x6
LED0_ON_H = 0x7
LED0_OFF_L = 0x8
LED0_OFF_H = 0x9

ALLLED_ON_L = 0xFA
ALLLED_ON_H = 0xFB
ALLLED_OFF_L = 0xFC
ALLLED_OFF_H = 0xFD

class PWMServoDriver:

  def __init__(self, i2cAddress = DEVICE_ADDRESS, i2cBus = DEVICE_BUS):
      self._i2cAddress = i2cAddress
      self._i2cBus = i2cBus
      self._bus = smbus.SMBus(i2cBus)

  def reset(self):
      bus.write_i2c_block_data(self._i2cAddress, PCA9685_MODE1, 0x0)

  def setPWMFreq(freq):
      freq *= 0.9                                                               # Correct for overshoot in the frequency setting (see issue #11).
      prescaleval = 25000000
      prescaleval /= 4096
      prescaleval /= freq
      prescaleval -= 1

      prescale = floor(prescaleval + 0.5)

      if (ENABLE_DEBUG_OUTPUT) {
        print("Final pre-scale: %f" % prescale)
      }

      oldmode = bus.read_i2c_block_data(self._i2cAddress, PCA9685_MODE1)
      newmode = (oldmode&0x7F) | 0x10                                           # sleep
      bus.write_i2c_block_data(self._i2cAddress, PCA9685_MODE1, newmode)        # go to sleep
      bus.write_i2c_block_data(self._i2cAddress, PCA9685_PRESCALE, prescale)    # set the prescaler
      bus.write_i2c_block_data(self._i2cAddress, PCA9685_MODE1, oldmode)
      time.sleep(5.0/1000.0)
      bus.write_i2c_block_data(self._i2cAddress, PCA9685_MODE1, oldmode | 0xa1) #  This sets the MODE1 register to turn on auto increment.
                                                                                # This is why the beginTransmission below was not working.
  def setPWM(num, on, off):
      bus.write_i2c_block_data(self._i2cAddress, LED0_ON_L+4*num, on)
      bus.write_i2c_block_data(self._i2cAddress, LED0_ON_L+4*num, on>>8)
      bus.write_i2c_block_data(self._i2cAddress, LED0_ON_L+4*num, off)
      bus.write_i2c_block_data(self._i2cAddress, LED0_ON_L+4*num, off>>8)

  def setPin(num, val, invert=False):
        # Clamp value between 0 and 4095 inclusive.
        val = min(val, 4095)
        if (invert):
            if (val == 0):
                # Special value for signal fully on.
                setPWM(num, 4096, 0)
            elif (val == 4095):
                # Special value for signal fully off.
                setPWM(num, 0, 4096)
            else:
                setPWM(num, 0, 4095-val)
        else:
            if (val == 4095):
              # Special value for signal fully on.
              setPWM(num, 4096, 0)
            elif (val == 0):
              # Special value for signal fully off.
              setPWM(num, 0, 4096)
            else:
              setPWM(num, 0, val)
