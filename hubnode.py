from datamodels.timeseriesdata import *
from vuwsn import *

class HubNode: 

    def __init__(self, description: str, origin: str, vuwsn: VUWSN):
        self.description = description
        self.origin = origin
        self.vuwsn = vuwsn

    def transmit(self) -> str:
        return self.vuwsn.get_data()


