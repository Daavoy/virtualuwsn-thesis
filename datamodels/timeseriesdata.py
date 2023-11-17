from datamodels.metadata import *
from typing import Any, Optional, List

import datetime


class Location(BaseModel):

    latitude: float
    longitude: float
    elevation: Optional[float]


class Observation(BaseModel):

    source: Optional[str]
    parameter: str
    value: Any
    unit: str
    qualityCode: int  # not optional, 0 is no quality control


class DataPoint(BaseModel):

    location: Optional[Location]
    time: datetime.datetime
    observations: List[Observation]


class TimeSeriesData(BaseModel):

    format: str  # identification of format
    metadata: MetaData
    data: List[DataPoint]

    def to_json_str(self) -> str:
        return self.json()


