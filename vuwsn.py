from datamodels.timeseriesdata import *
from sensor import *
from abc import abstractmethod
import os

class VUWSN: 
    def __init__(self, description: str):
        self.description = description

    @abstractmethod
    def get_data(self) -> str:
        pass

class SmartOceanVUWSN(VUWSN):

    def __init__(self, description: str, origin: str, timeseries: str, location: Location, sensors: List[Sensor]):
        super().__init__(description)
        self.origin = origin
        self.timeseries = timeseries
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

    def get_data(self) -> str:
        return self.generate_timeseries_data_json()
    
class TempCondBattVUWSN(SmartOceanVUWSN):

    def __init__(self, name:str, location: Location):
        temp_sensor = TemperatureSensor("Virtual Temperature Sensor")
        cond_sensor = ConductivitySensor("Virtual Conductivity Sensor")
        batt_sensor = BatterySensor("Virtual Battery Sensor")

        super().__init__(description=name, timeseries=name,
                         origin=name, location=location,
                         sensors=[temp_sensor, cond_sensor, batt_sensor])

class FileVUWSN(VUWSN):

    def __init__(self, description: str, data_path: str):
        super().__init__(description)
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

    def get_data(self) -> str:
        return self.generate_data()
