from sensor import *
from hubnode import *


class VirtualSensorHubNode(SensorHubNode):

    def __init__(self, name: str, location: Location):

        temp_sensor = TemperatureSensor("Virtual Temperature Sensor")
        cond_sensor = ConductivitySensor("Virtual Conductivity Sensor")
        batt_sensor = BatterySensor("Virtual Battery Sensor")

        super().__init__(description=name, timeseries=name,
                         origin=name, location=location,
                         sensors=[temp_sensor, cond_sensor, batt_sensor])
