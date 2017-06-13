import time

import motormanager
import pantiltmanager

class CollisionManager(object):
    def __init__(self, panTiltManager, motorManager):
        self.panTiltManager = panTiltManager
        self.motorManager = motorManager

        self.calibrationEvents = []
        self.inCalibration = False
        self.calibrate()


    def calibrate(self):
        motorManager.block()
        self.inCalibration = True
        time.sleep(10)
        self.analyzeCalibrationEvents()
        self.inCalibration = False
        motorManager.unblock()

    def analyzeCalibrationEvents(self):
        if not calibrationEvents:
            return

        countLeft = 0
        countRight = 0
        for event in self.calibrationEvents
            if event.leftSensor:
                countLeft += 1

            if event.rightSensor:
                countRight += 1

        self.avgLeft = countLeft / len(self.calibrationEvents)
        self.avgRight = countRight / len(self.calibrationEvents)

    def processEvent(self, event):
        if inCalibration:
            calibrationEvents.append(event)
            return
