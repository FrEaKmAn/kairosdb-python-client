import unittest
from kairosdbclient.exceptions import ResponseException
from kairosdbclient.rest.apirequests import *

from kairosdbclient import KairosDBRestClient
from kairosdbclient.rest.apirequests.query_metric_names import QueryMetricNamesRequest
from kairosdbclient.rest.apirequests.query_metric_tags import MetricTag
from kairosdbclient.rest.metric import Metric
from mock import patch
from tests.tools import MockResponse, MockAPIRequest


class RestClientTest(unittest.TestCase):
    def setUp(self):
        self.client = KairosDBRestClient()

    def test_creating_url(self):
        url = self.client._get_url('health/status')

        self.assertEqual(url, 'http://127.0.0.1:8080/api/v1/health/status')

    def test_get_item(self):
        single_metric = self.client[1:2, 'metric.name']

        self.assertEqual(single_metric.start, 1)
        self.assertEqual(single_metric.end, 2)
        self.assertEqual(len(single_metric.metrics), 1)
        self.assertEqual(single_metric.metrics[0].name, 'metric.name')

    def test_get_item_with_multiple_metrics(self):
        single_metric = self.client[1:2, ['metric.name', 'metric.name2']]

        self.assertEqual(len(single_metric.metrics), 2)
        self.assertEqual(single_metric.metrics[0].name, 'metric.name')
        self.assertEqual(single_metric.metrics[1].name, 'metric.name2')

    def test_parse_response_success_status_code(self):
        response = MockResponse(status_code=204)

        with patch.object(MockAPIRequest, 'to_resource') as mock_method:
            api_request = MockAPIRequest(success_status_code=204)
            self.client._parse_response(api_request, response)

        mock_method.assert_called_once_with(response)

    def test_should_fail_if_response_status_code_and_resource_success_status_code_do_not_match(self):
        response = MockResponse(status_code=500, text="Server error")
        api_request = MockAPIRequest(success_status_code=204)

        with self.assertRaises(ResponseException):
            self.client._parse_response(api_request, response)

    def test_version(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.version()

        mock_method.assert_called_once_with('GET', VersionRequest())

    def test_metric_tags(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.metric_tags(100, 200, [MetricTag('metric.1', host=['azure'])])

        mock_method.assert_called_once_with('POST', QueryMetricTagsRequest(100, 200, [MetricTag('metric.1', host=['azure'])]))

    def test_metric_names(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.metric_names()

        mock_method.assert_called_once_with('GET', QueryMetricNamesRequest())

    def test_tag_names(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.tag_names()

        mock_method.assert_called_once_with('GET', QueryTagNamesRequest())

    def test_tag_values(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.tag_values()

        mock_method.assert_called_once_with('GET', QueryTagValuesRequest())

    def test_delete_metric(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.delete_metric('metric.name')

        mock_method.assert_called_once_with('DELETE', DeleteMetricRequest('metric.name'))

    def test_health_check(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.health_check()

        mock_method.assert_called_once_with('GET', HealthCheckRequest())

    def test_health_status(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.health_status()

        mock_method.assert_called_once_with('GET', HealthStatusRequest())

    def test_query(self):
        with patch.object(KairosDBRestClient, '_make_request') as mock_method:
            client = KairosDBRestClient()
            client.query(100, 200, metrics=[Metric('metric.name')])

        mock_method.assert_called_once_with('POST', QueryMetricDataPointsRequest(100, 200, [Metric('metric.name')], None, 0))