#!/usr/local/bin/python

import motormanager
import pantiltmanager
import keyreader


motorManager = motormanager.MotorManager(120, 5)
panTiltManager = pantiltmanager.PanTiltManager()

val = ''
while (val != 'q'):
  val = keyreader.read_single_keypress()
  if (val == 'w'):
    panTiltManager.tiltTo(panTiltManager.getTiltPosition() + 5)
  elif (val == 's'):
    panTiltManager.tiltTo(panTiltManager.getTiltPosition() - 5)
  elif (val == 'a'):
    panTiltManager.panTo(panTiltManager.getPanPosition() + 5)
  elif (val =='d'):
    panTiltManager.panTo(panTiltManager.getPanPosition() - 5)

  print panTiltManager.getPanPosition()
  print panTiltManager.getTiltPosition()
