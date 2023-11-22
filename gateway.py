from hubnode import *
import time

class Gateway:

    def __init__(self, name, sensorhub: HubNode):
        self.name = name
        self.hub = sensorhub

    def run(self, count, sleep_time, publish):

        for i in range(1, count+1):
            data = self.hub.transmit()

            if publish:
                publish(data,i)
            else:
                print(f'Client - not transmitting') # use logger instead

            time.sleep(sleep_time)





