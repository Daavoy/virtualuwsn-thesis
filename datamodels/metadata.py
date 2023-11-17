from pydantic import BaseModel


class MetaData(BaseModel):

    description: str
    timeseries: str     # identification of the time series
    origin: str         # where do the data originate from (traceability) - optional as it could also be in the data point
