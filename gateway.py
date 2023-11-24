from hubnode import *
import time

class Gateway:

    def __init__(self, name, sensorhubs: list[HubNode]=list()):
        self.name = name
        self.hubs = sensorhubs

    def run(self, count, sleep_time, publish):
        hub_idx = 0

        for i in range(1, count+1):
            hub = self.hubs[hub_idx]
            data = hub.transmit()

            if publish:
                publish(data,i)
            else:
                print(f'Hub ({hub.description}) - not transmitting') # use logger instead

            hub_idx = (hub_idx + 1) % len(self.hubs)

            time.sleep(sleep_time)

    # TODO: Add method to add/remove hubs to gateway?






