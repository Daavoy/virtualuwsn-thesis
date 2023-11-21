from sensor import Sensor
from typing import List
import os

from datamodels.timeseriesdata import *

from abc import abstractmethod

class HubNode: 

    def __init__(self, description: str, origin: str, timeseries: str):
        self.description = description
        self.origin = origin
        self.timeseries = timeseries

    @abstractmethod
    def transmit(self) -> str:
        pass

class SensorHubNode(HubNode):

    def __init__(self, description: str, origin: str, timeseries: str, location: Location, sensors: List[Sensor]):
        super().__init__(description, origin, timeseries)
        self.location = location
        self.sensors = sensors

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
        return ts_data.json(indent=4)

    def transmit(self) -> str:
        return self.generate_timeseries_data_json()
    

class DataFileHubNode(HubNode):

    def __init__(self, description: str, origin: str, timeseries: str, data_path: str):
        super().__init__(description, origin, timeseries)
        self.data_path = data_path
        self.data_files = [f for f in os.listdir(self.data_path) if os.path.isfile(os.path.join(self.data_path, f))]
        self.current_file_index = 0

    def generate_data(self) -> str:
        if(len(self.data_files) == 0):
            raise Exception(f"No data files found in '{self.data_path}'")
        if(self.current_file_index >= len(self.data_files)): self.current_file_index = 0 

        data_file_name = self.data_files[self.current_file_index]
        data_file_path = os.path.join(self.data_path, data_file_name)

        with open(data_file_path, 'r') as data_file:
            test_data = data_file.read()
        
        self.current_file_index = (self.current_file_index + 1) % len(self.data_files)
        return test_data

    def transmit(self) -> str:
        return self.generate_data()

