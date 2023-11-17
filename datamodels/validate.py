import pydantic
import json

from timeseriesdata import TimeSeriesData


class ValidateException(Exception):

    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return self.message


def validate_ts_format(ts_json_str: str) -> bool:

    try:
        json_item = json.loads(ts_json_str)

    except json.JSONDecodeError as exc:
        raise ValidateException(f'JSONDecodeError: Invalid JSON: {exc.msg}, line {exc.lineno}, column {exc.colno}')

    try:
        TimeSeriesData(**json_item)

    except pydantic.ValidationError as exc:
        raise ValidateException(f'PYDANTIC ValidationError: Invalid schema: {exc}')

    return True
