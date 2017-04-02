from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import random
import time

class DataRecorder:
    def __init__(self, measurement, user, password, host='localhost', port=8086, dbname='trevor'):
        self.client = InfluxDBClient(host, port, user, password, dbname)
        self.measurement = measurement

    def recordValue(self, value):
        pointValues = [{
                "time": datetime.datetime.today().strftime ("%Y-%m-%d %H:%M:%S"),
                # "time": int(past_date.strftime('%s')),
                "measurement": self.measurement,
                'fields':  {
                    'value': value,
                },
            }]
        self.client.write_points(pointValues)

    def record(self, data):
        self.client.write_points(data)

