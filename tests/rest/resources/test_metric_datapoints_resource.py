import unittest
from kairosdbclient.rest.resources.metric_datapoints import MetricDataPoints
from tests.tools import MockResponse, get_resource_as_json


class MetricDataPointsResourceTest(unittest.TestCase):
    def setUp(self):
        request = None
        response = MockResponse(json_content=get_resource_as_json('metric_datapoints.json'))
        self.resource = MetricDataPoints(request, response)

    def test_queries(self):
        self.assertEqual(len(self.resource.queries), 1)

    def test_sample_size(self):
        self.assertEqual(self.resource.queries[0].sample_size, 2)