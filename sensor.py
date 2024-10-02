import math
import time

from sfisop.datamodels.tsdatamodel.timeseriesdata import *

from abc import abstractmethod

# Base class for all sensors
class Sensor:

    def __init__(self, source: str, source_id, parameter: str, unit: str):
        self.source = source
        self.source_id = source_id
        self.parameter = parameter
        self.unit = unit

    @abstractmethod
    def simulate_value(self) -> str:
        pass

    def read(self) -> str:
        pass
    

# VirtualSensor class for custom generated sensor data in the TimeSeriesData format
class VirtualSensor(Sensor):

    def __init__(self, source: str, source_id:str, parameter: str, unit: str):
        super().__init__(source, source_id, parameter, unit)

    @abstractmethod
    def simulate_value(self) -> str:
        pass

    def read(self) -> Observation:
        NO_DATAQUALITY_CODE = 0

        obs = Observation(source=self.source,
                          source_id=self.source_id,
                          parameter=self.parameter,
                          value=self.simulate_value(),
                          unit=self.unit,
                          qualityCodes=[NO_DATAQUALITY_CODE])

        return obs


class TemperatureSensor(VirtualSensor):

    def __init__(self, source: str, source_id: str):
        super().__init__(source, source_id,  "sea_water_temperature", "degrees_C")

    def simulate_value(self) -> str:

        TEMPERATURE_RANGE = 20
        t = time.time() / 10
        temp = round(math.sin(t) * TEMPERATURE_RANGE, 1)

        return str(temp)


class ConductivitySensor(VirtualSensor):

    def __init__(self, source: str, source_id:str):
        super().__init__(source, source_id, "sea_water_electrical_conductivity", "S m-1")

    def simulate_value(self) -> str:

        CONDUCTIVITY_RANGE = 3
        t = time.time() / 10
        cond = round(abs(math.cos(t)) * CONDUCTIVITY_RANGE, 1)

        return str(cond)


class BatterySensor(VirtualSensor):

    def __init__(self, source: str, source_id:str):
        super().__init__(source, source_id, "battery_level", "percentage") # TODO: Need standard here (see issue 9)

    def simulate_value(self) -> str:

        BATTERY_RANGE = 100
        t = time.time() / 10
        batt = round(((t % BATTERY_RANGE) / 10), 1)

        return str(batt)
