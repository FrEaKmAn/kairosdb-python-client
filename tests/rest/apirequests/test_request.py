import unittest
import pytz
from kairosdbclient.exceptions import RequestException
from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources.base import Resource
from datetime import datetime


class MockResource(Resource):
    pass


class MockRequest(Request):
    uri = 'uri'
    resource = MockResource
    success_status_code = 200
    request_method = 'GET'

    def payload(self):
        return None


class RequestTest(unittest.TestCase):
    def setUp(self):
        self.request = MockRequest()

    def test_format_time_as_int(self):
        start_time = self.request._format_time('start', 100)

        self.assertEqual(start_time, {'start_absolute': 100})

    def test_format_time_as_list(self):
        start_time = self.request._format_time('start', (2, 'days'))

        self.assertEqual(start_time, {'start_relative': {'value': 2, 'unit': 'days'}})

    def test_format_time_as_datetime(self):
        time = datetime(year=2016, month=1, day=1, hour=5, minute=0, second=0)
        start_time = self.request._format_time('start', time)

        self.assertEqual(start_time, {'start_absolute': 1451624400000})

    def test_format_time_as_datetime_with_timezone(self):
        time = datetime(2016, 1, 1, 5)
        time = pytz.timezone('Europe/Ljubljana').localize(time)
        start_time = self.request._format_time('start', time)

        self.assertEqual(start_time, {'start_absolute': 1451620800000})

    def test_should_fail_if_invalid_time_format(self):
        with self.assertRaises(RequestException):
            self.request._format_time('start', 'invalid_format')
