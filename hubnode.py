from datamodels.tsdatamodel.metadata import *
from datamodels.tsdatamodel.timeseriesdata import *

from sensor import Sensor
from vuwsn import *
from datetime import datetime
from abc import abstractmethod


class HubNode:

    def __init__(self, description: str, origin: str):
        self.description = description
        self.origin = origin

    @abstractmethod
    def transmit(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> str:
        pass


class FileHubNode(HubNode):

    def __init__(self, description: str, origin: str, data_path: str):
        super().__init__(description, origin)
        self.data_file_path = data_path

    def transmit(self) -> str:
        return self.get_data()

    def get_data(self) -> str:

        with open(self.data_file_path, 'r') as data_file:
            test_data = data_file.read()

        return test_data


class TempCondBattNode(HubNode):

    def __init__(self, description: str, format: str,
                 origin: str, timeseries: str,
                 source: str, source_id: str,
                 location: Location, sensors: List[Sensor]):

        super().__init__(description, origin)
        self.format = format
        self.origin = origin
        self.timeseries = timeseries
        self.source = source
        self.source_id = source_id
        self.location = location
        self.sensors = sensors
        self.dp_id_count = 1

    def generate_datapoint(self) -> DataPoint:
        obs = [sensor.read() for sensor in self.sensors]
        time_now = datetime.now()
        time_now_local = time_now.astimezone()

        data_point = DataPoint(dp_id=str(self.dp_id_count),
                               source=self.source,
                               source_id=self.source_id,
                               location=self.location,
                               time=datetime.isoformat(time_now_local),
                               observations=obs)

        self.dp_id_count = self.dp_id_count + 1

        return data_point

    def generate_timeseries_data(self) -> TimeSeriesData:
        data_point = self.generate_datapoint()
        data_points = [data_point]

        meta_data = MetaData(description=self.description,
                             timeseries=self.timeseries,
                             origin=self.origin)

        ts_data = TimeSeriesData(format=self.format, metadata=meta_data,
                                 datapoints=data_points, data=data_points)

        return ts_data

    def generate_timeseries_data_json(self) -> str:
        ts_data = self.generate_timeseries_data()
        return ts_data.json(indent=4)

    def get_data(self) -> str:
        return self.generate_timeseries_data_json()

    def transmit(self) -> str:
        return self.get_data()