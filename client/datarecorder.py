from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import random
import time

class DataRecorder:
    def __init__(self, user, password, host='localhost', port=8086, dbname='trevor'):
        self.client = InfluxDBClient(host, port, user, password, dbname)

    def getValue(self, measurement, value):
        return {
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                # "time": int(past_date.strftime('%s')),
                "measurement": measurement,
                'fields':  {
                    'value': value,
                },
            }

    def record(self, values):
        results = []
        for val in values:
            for k, v in val.items():
                results.append(self.getValue(k,v))
        self.client.write_points(results)
