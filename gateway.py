from hubnode import *
import time
import hashlib
from utils.log_utils import getFileHandler
from paho.mqtt.properties import Properties, PacketTypes

class Gateway:

    def __init__(self, name, sensorhubs: list[HubNode]=list()):
        self.name = name
        self.hubs = sensorhubs

        # Setup logging
        self.logger = getFileHandler("logs/gateway")

        self.log(self.__str__())

    def __str__(self) -> str:
        return ''.join((f'Gateway Configuration: \n',
                        f'Name: {self.name} \n',
                        f'Sensorhubs: {len(self.hubs)}'))

    def log(self, msg: str):
        self.logger.info(msg)

    def run(self, count, publish_interval, publisher):
        nr_of_failed_transmits = 0  
        hub_idx = 0
        time.sleep(2) # wait before starting simulation
        self.log(f"Starting publishing {count} messages with {publish_interval} second intervals")

        for i in range(1, count+1):
            hub = self.hubs[hub_idx]
            data = hub.transmit()

            if publisher.do_continue:
                # Add properties for analytics
                data_to_hash = f"{i}{time.time()}"
                id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                publish_properties = Properties(PacketTypes.PUBLISH) 
                publish_properties.UserProperty = ("unique_message_id", str(id)) 
                publish_properties.UserProperty = ("publisher_send_time", str((time.time()*1000)))

                if publisher.publish(data, publish_properties):
                    self.log(f'Hub ({hub.description}) - transmitted data')
                else:
                    self.log(f'Hub ({hub.description}) - failed to transmit data')
                    nr_of_failed_transmits += 1
            else:
                self.log(f'Hub ({hub.description}) - not transmitting')
                nr_of_failed_transmits += 1

            hub_idx = (hub_idx + 1) % len(self.hubs)

            time.sleep(publish_interval)

        self.log(f'Gateway finished transmitting data. Transmitted {count - nr_of_failed_transmits}/{count} messages')
        publisher.stop()

    # TODO: Add method to add/remove hubs to gateway?






