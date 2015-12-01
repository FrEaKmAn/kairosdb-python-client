import unittest
from kairosdbclient.rest.resources.metric_tags import MetricTags
from tests.tools import get_resource_as_json, MockResponse


class MetricTagsResourceTest(unittest.TestCase):
    def test_parsing_response(self):
        json = get_resource_as_json('metric_tags.json')
        resource = MetricTags(MockResponse(json_content=json))

        self.assertEqual(len(resource.results), 1)