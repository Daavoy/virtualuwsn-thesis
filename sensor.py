import math
import time

from datamodels.timeseriesdata import *

from abc import abstractmethod


class Sensor:

    def __init__(self, source: str, parameter: str, unit: str):
        self.source = source
        self.parameter = parameter
        self.unit = unit

    @abstractmethod
    def simulate_value(self) -> str:
        pass

    def read(self) -> Observation:

        NO_DATAQUALITY_CODE = 0

        obs = Observation(source=self.source,
                          parameter=self.parameter,
                          value=self.simulate_value(),
                          unit=self.unit,
                          qualityCode=NO_DATAQUALITY_CODE)

        return obs


class TemperatureSensor(Sensor):

    def __init__(self, source: str):
        super().__init__(source, "temperature", "degree celcius")

    def simulate_value(self) -> str:

        TEMPERATURE_RANGE = 20
        t = time.time() / 10
        temp = round(math.sin(t) * TEMPERATURE_RANGE, 1)

        return str(temp)


class ConductivitySensor(Sensor):

    def __init__(self, source: str):
        super().__init__(source, "conductivity", "S/m")

    def simulate_value(self) -> str:

        CONDUCTIVITY_RANGE = 3
        t = time.time() / 10
        cond = round(abs(math.cos(t)) * CONDUCTIVITY_RANGE, 1)

        return str(cond)


class BatterySensor(Sensor):

    def __init__(self, source: str):
        super().__init__(source, "battery level", "percentage")

    def simulate_value(self) -> str:

        BATTERY_RANGE = 100
        t = time.time() / 10
        batt = round(((t % BATTERY_RANGE) / 10), 1)

        return str(batt)
