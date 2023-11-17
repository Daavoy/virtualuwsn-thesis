from hubnode import *


class Gateway:

    def __init__(self, name, sensorhub: SensorHubNode):
        self.name = name
        self.hub = sensorhub

    def run(self, count, sleep_time, transmit):

        for i in range(1, count+1):
            ts_data_str = self.hub.transmit()
            logging.info(f'{ts_data_str}')

            if transmit:
                transmit(ts_data_str)
            else:
                logging.info(f'Client - not transmitting')

            time.sleep(sleep_time)


