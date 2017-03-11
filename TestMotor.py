#!/usr/local/bin/python

import motormanager
import keyreader


motorManager = motormanager.MotorManager(120, 5)
val = ''
while (val != 'q'):
  val = keyreader.read_single_keypress()
  print val
  if (val == 'w'):
    motorManager.forward(0.5)
  elif (val == 's'):
    motorManager.backward(0.5)
  elif (val == 'a'):
    motorManager.left(0.5)
  elif (val =='d'):
    motorManager.right(0.5)
  else:
    motorManager.stop()
