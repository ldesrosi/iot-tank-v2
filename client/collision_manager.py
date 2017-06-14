import time
import random

import motormanager
import pantiltmanager

class CollisionManager(object):
    def __init__(self, panTiltManager, motorManager, max_rpm, wheel_diameter, tank_diameter):
        self.panTiltManager = panTiltManager
        self.motorManager = motorManager

        self.max_rpm = max_rpm
        self.wheel_circumference = wheel_diameter * math.pi
        self.tank_circumference = tank_circumference * math.pi


    def processEvent(self, event):
        blockId = random.random()
        if event.leftSensor or event.rightSensor:
            motorManager.block(blockId)
            if event.leftSensor:
                self.turnRight(blockId)
            else event.rightSensor:
                self.turnLeft(blockId)
            motorManager.unblock(blockId)

    def turnLeft(self, angle, blockId=None):
        power = 0.5
        duration = calculateTurnDuration(90, angle, power)
        self.motorManager.left(power, blockId)
        time.sleep(duration)
        self.motorManager.stop()

    def turnRight(self, angle, blockId=None):
        power = 0.5
        duration = calculateTurnDuration(90, angle, power)
        self.motorManager.right(power, blockId)
        time.sleep(duration)
        self.motorManager.stop()

    def calculateTurnDuration(self, angle, power):
        rps = self.max_rpm * power
        duration_rot = 1/rps

        target_distance = (angle/360)*self.tank_circumference
        target_duration = (target_distance/self.wheel_circumference)*duration_rot

        return target_duration
