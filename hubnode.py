
from sensor import Sensor
from typing import List

from datamodels.timeseriesdata import *

import logging
import time

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")


class SensorHubNode:

    def __init__(self, description: str, origin: str, timeseries: str, location: Location, sensors: List[Sensor]):
        self.description = description
        self.origin = origin
        self.location = location
        self.sensors = sensors
        self.timeseries = timeseries

    def generate_datapoint(self) -> DataPoint:

        obs = [sensor.read() for sensor in self.sensors]

        time_now = datetime.datetime.now()

        time_now_local = time_now.astimezone()

        data_point = DataPoint(location=self.location,
                               time=time_now_local,
                               observations=obs)

        return data_point

    def generate_timeseries_data(self) -> TimeSeriesData:

        SMARTOCEAN_FORMAT = "SMARTOCEAN_V0"

        data_point = self.generate_datapoint()

        data_points = [data_point]

        meta_data = MetaData(description=self.description,
                             timeseries=self.timeseries,
                             origin=self.origin)

        ts_data = TimeSeriesData(format=SMARTOCEAN_FORMAT, metadata=meta_data,
                                 datapoints=data_points, data=data_points)

        return ts_data

    def generate_timeseries_data_json(self) -> str:

        ts_data = self.generate_timeseries_data()

        return ts_data.json()

    def transmit(self) -> str:

        return self.generate_timeseries_data_json()

    def run(self, count, sleep_time):

        for i in range(1, count):
            ts_data = self.generate_timeseries_data_json()
            logging.info(f'{ts_data}')

            time.sleep(sleep_time)
