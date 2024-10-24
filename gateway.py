import uuid
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
        self.logger = getFileHandler(f"logs/{self.name}")

        self.log(self.__str__())

    def __str__(self) -> str:
        return ''.join((f'Gateway Configuration: \n',
                        f'Name: {self.name} \n',
                        f'Sensorhubs: {len(self.hubs)}'))

    def log(self, msg: str):
        self.logger.info(msg)

    def run(self, publisher):
        nr_of_failed_transmits = 0  
        #hub_idx = 0
        #time.sleep(2) # wait before starting simulation

        for i, hub in enumerate(self.hubs):
            self.log(f"Starting publishing messages from sensor hub {hub.description}")
            data = hub.transmit()

            if publisher.do_continue:
                # Add properties for analytics
                pid = os.getpid()
                random_uuid = uuid.uuid4()
                data_to_hash = f"{i}{time.time()}{data}{pid}{random_uuid}"
                id = hashlib.sha256(data_to_hash.encode()).hexdigest()

                publish_properties = Properties(PacketTypes.PUBLISH) 
                publish_properties.UserProperty = ("unique_message_id", str(id)) 
                publish_properties.UserProperty = ("publisher_send_time", str((time.time()*1000)))
                publish_properties.UserProperty = ("order", str(i))

                if publisher.publish(data, publish_properties):
                    self.log(f'Hub ({hub.description}) - transmitted data')
                else:
                    self.log(f'Hub ({hub.description}) - failed to transmit data')
                    nr_of_failed_transmits += 1
            else:
                self.log(f'Hub ({hub.description}) - not transmitting')
                nr_of_failed_transmits += 1

            #hub_idx = (hub_idx + 1) % len(self.hubs)

        self.log(f'Gateway finished transmitting data. Transmitted {len(self.hubs) - nr_of_failed_transmits}/{len(self.hubs)} messages')
        publisher.stop()

    # TODO: Add method to add/remove hubs to gateway?






