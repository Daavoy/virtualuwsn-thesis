from gateway import Gateway
from hubnode import HubNode, TempCondBattNode
from sensor import *
from abc import abstractmethod
import os


class VUWSN: 
    def __init__(self, description: str):
        self.description = description
        self.sinks = list()

    @abstractmethod
    def get_gateways(self) -> list[Gateway]:
        pass


class SmartOceanVUWSN(VUWSN):
    """
    Basic sensor network setup with one gateway and one sensor hub that has 3 simulated sensors.
    """
    def __init__(self, description: str, format: str,
                 origin: str, timeseries: str,
                 source: str, source_id: str,
                 location: Location):

        temp_sensor = TemperatureSensor("Virtual Temperature Sensor", "0001")
        cond_sensor = ConductivitySensor("Virtual Conductivity Sensor", "0002")
        batt_sensor = BatterySensor("Virtual Battery Sensor", "0003")

        basic_node = TempCondBattNode(description=description, timeseries=timeseries, format=format, source=source,
                                      source_id=source_id, origin=origin, location=location,
                                      sensors=[temp_sensor, cond_sensor, batt_sensor])

        self.gateway = Gateway(name="gateway", sensorhubs=[basic_node])

    def get_gateways(self) -> list[Gateway]:
        return [self.gateway]


class FileVUWSN(VUWSN):
    """
    Creates a gateway for each sub_folder and a hub node for each file in the gateway data path (sub folder).
    Each historic data file represent a set of measurement that are sent by a hub to a gateway and transmitted
    to the cloud-side.
    """

    def __init__(self, description: str, data_path: str):
        super().__init__(description)
        self.data_path = data_path
        self.folders   = [f for f in os.listdir(self.data_path) if os.path.isdir(os.path.join(self.data_path, f))]

    def get_gateways(self) -> list[Gateway]:
        """
        Populates the sinks attribute of UWSN objects according to the file structure passed in the configuration.
        Returns: self.sinks list of Gateway objects.
        """
        for idx, sink in enumerate(self.folders):
            hubnodes = list()

            for i, file in enumerate(os.listdir(sink)):
                if os.path.isfile(os.path.join(self.data_path, file)):
                    origin = '.'.join((os.path.basename(self.data_path), sink, f'hub{i+1}'))
                    filepath = os.path.join(self.data_path, file)
                    node = HubNode(f"Hub {idx + 1}: for historic data", origin, filepath)
                    hubnodes.append(node)

            gateway = Gateway(f"{'.'.join((os.path.basename(self.data_path), sink))}", hubnodes)
            self.sinks.append(gateway)

        return self.sinks

    # def generate_data(self) -> str:
    #     if(len(self.data_files) == 0):
    #         raise Exception(f"No data files found in '{self.data_path}'")
    #     if(self.current_file_index >= len(self.data_files)): self.current_file_index = 0
    #
    #     data_file_name = self.data_files[self.current_file_index]
    #     data_file_path = os.path.join(self.data_path, data_file_name)
    #
    #     with open(data_file_path, 'r') as data_file:
    #         test_data = data_file.read()
    #
    #     self.current_file_index = (self.current_file_index + 1) % len(self.data_files)
    #     return test_data
    # def get_data(self) -> str:
    #    return self.generate_data()

