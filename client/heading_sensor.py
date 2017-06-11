import time
import threading
import Adafruit_LSM9DS0

class HeadingManager(threading.Thread):

    def __init__(self, dataRecorder=None):
        threading.Thread.__init__(self)
	self.done = False
        self.imu = Adafruit_LSM9DS0.LSM9DS0()
        self.dataRecorder = dataRecorder

    def stop(self):
        self.done=True

    def run(self):
        print('[heading: starting to capture heading data]')
        while not self.done:
            # Grab (x, y, z) readings for gyro, mag and accelerometer
            gyro, mag, accel = self.imu.read()
            internal_temp = self.imu.rawTemp() 

            # Unpack tuples
            gyro_x, gyro_y, gyro_z = gyro
            mag_x, mag_y, mag_z = mag
            accel_x, accel_y, accel_z = accel

            self.dataRecorder.record([{"gyro_x":float(gyro_x)},{"gyro_y":float(gyro_y)},{"gyro_z":float(gyro_z)}])
            self.dataRecorder.record([{"mag_x":float(mag_x)},{"mag_y":float(mag_y)},{"mag_z":float(mag_z)}])
            self.dataRecorder.record([{"accel_x":float(accel_x)},{"accel_y":float(accel_y)},{"accel_z":float(accel_z)}])
            self.dataRecorder.record([{"temp":internal_temp}])

            # Wait half a second before repeating
            time.sleep(0.5)
        print('[heading: shutting down heading capture]')
