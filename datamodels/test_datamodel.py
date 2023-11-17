import unittest
import json

from timeseriesdata import *
from testdatajson import *

import validate


def create_ts_data():

        a_location = Location(latitude=5.0, longitude=65, elevation=2.0)

        meta_data = MetaData(description="test example data", timeseries="austevoll south", origin="sensorhub south")

        observation = Observation(source="AADI TEMP SENSOR", parameter="temperature", value="5.0", unit="celcius",
                                  qualityCode=0)

        data_point = DataPoint(location=a_location, time=datetime.datetime.now(), observations=[observation])

        data_points = [data_point]

        ts_data = TimeSeriesData(format="test format", metadata=meta_data, datapoints=data_points, data=data_points)

        return ts_data


class TestDataModel(unittest.TestCase):

    def test_create_ts_data(self):

        ts_data = create_ts_data()
        self.assertIsNotNone(ts_data)

    def test_json_validate(self):
        ts_data = create_ts_data()
        ts_data_json = ts_data.to_json_str()

        try:
            res = validate.validate_ts_format(ts_data_json)
            self.assertTrue(res)
        except validate.ValidateException as exc:
            self.fail(f'{exc.message}')

    def test_ts_data_invalid(self):
        ts_data_err_str = json.dumps(ts_testdata_err)

        try:
            res = validate.validate_ts_format(ts_data_err_str)
        except validate.ValidateException as exc:
            self.assertTrue(True)
        else:
            self.fail('test_json_invalid')

    def test_json_invalid(self):
        json_err_str = '{"name": "Joe", "age": "null", }'

        try:
            res = validate.validate_ts_format(json_err_str)
        except validate.ValidateException as exc:
            self.assertTrue(True)
        else:
            self.fail('test_json_invalid')


if __name__ == '__main__':
    unittest.main()

