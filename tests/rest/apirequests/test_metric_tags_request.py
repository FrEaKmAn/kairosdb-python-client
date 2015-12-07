import unittest
from kairosdbclient.exceptions import RequestException
from kairosdbclient.rest.apirequests.query_metric_tags import QueryMetricTagsRequest, MetricTag
from kairosdbclient.rest.resources.metric_tags import MetricTags


class MetricTagsRequestTest(unittest.TestCase):
    def test_metric_tags_request(self):
        request = QueryMetricTagsRequest(100, 200, metrics=[MetricTag('metric.1', host=['azure'])])

        self.assertEqual(request.payload(), {'start_absolute': 100,
                                             'end_absolute': 200,
                                             'metrics': [
                                                 {'name': 'metric.1',
                                                  'tags': {
                                                      'host': ['azure']
                                                  }}
                                             ]})
        self.assertEqual(request.resource, MetricTags)
        self.assertEqual(request.success_status_code, 200)
        self.assertEqual(request.uri, 'datapoints/query/tags')

    def test_metric_tags_as_dict(self):
        request = QueryMetricTagsRequest(100, 200, metrics=[{'name': 'metric.1', 'tags': {'host': ['azure']}}])

        self.assertEqual(request.payload(), {'start_absolute': 100,
                                             'end_absolute': 200,
                                             'metrics': [
                                                 {'name': 'metric.1',
                                                  'tags': {
                                                      'host': ['azure']
                                                  }}
                                             ]})

    def test_should_fail_if_metric_tags_dict_is_missing_metric_name(self):
        with self.assertRaises(RequestException):
            QueryMetricTagsRequest(100, 200, metrics=[{'tags': {'host': ['azure']}}])

    def test_metric_tag_without_tags(self):
        request = QueryMetricTagsRequest(100, 200, metrics=[{'name': 'metric.1'}])

        self.assertEqual(request.payload(), {'start_absolute': 100,
                                             'end_absolute': 200,
                                             'metrics': [
                                                 {'name': 'metric.1'}
                                             ]})


class MetricTagTest(unittest.TestCase):
    def test_metric_tag(self):
        metric_tag = MetricTag('metric.1', host=['azure'])

        self.assertEqual(metric_tag.name, 'metric.1')
        self.assertEqual(metric_tag.tags, {'host': ['azure']})

    def test_metric_tag_with_tag_value_as_string(self):
        metric_tag = MetricTag('metric.1', host='azure')

        self.assertEqual(metric_tag.name, 'metric.1')
        self.assertEqual(metric_tag.tags, {'host': ['azure']})

    def test_metric_tag_without_tags(self):
        metric_tag = MetricTag('metric.1')

        self.assertEqual(metric_tag.name, 'metric.1')
        self.assertEqual(metric_tag.tags, {})