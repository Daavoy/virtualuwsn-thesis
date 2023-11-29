from hubnode import *
import time
import hashlib
from utils.log_utils import getFileHandler

class Gateway:

    def __init__(self, name, sensorhubs: list[HubNode]=list()):
        self.name = name
        self.hubs = sensorhubs

        # Setup publisher logging
        self.logger = getFileHandler("logs/gateway")

        self.log(self.__str__())

    def __str__(self) -> str:
        return ''.join((f'Gateway Configuration: \n',
                        f'Name: {self.name} \n',
                        f'Sensorhubs: {len(self.hubs)}'))

    def log(self, msg: str):
        self.logger.info(msg)

    def run(self, count, sleep_time, publish):
        nr_of_failed_transmits = 0  
        hub_idx = 0
        time.sleep(10) # wait before starting simulation

        for i in range(1, count+1):
            hub = self.hubs[hub_idx]
            data = hub.transmit()

            if publish:
                data_to_hash = f"{i}{time.time()}"
                id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                if publish(data,id):
                    self.log(f'Hub ({hub.description}) - transmitted data')
                else:
                    self.log(f'Hub ({hub.description}) - failed to transmit data')
                    nr_of_failed_transmits += 1
            else:
                self.log(f'Hub ({hub.description}) - not transmitting')
                nr_of_failed_transmits += 1

            hub_idx = (hub_idx + 1) % len(self.hubs)

            time.sleep(sleep_time)

        self.log(f'Gateway finished transmitting data. Transmitted {count - nr_of_failed_transmits}/{nr_of_failed_transmits} messages')

    # TODO: Add method to add/remove hubs to gateway?






