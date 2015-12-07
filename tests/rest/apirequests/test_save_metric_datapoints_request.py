import unittest
from kairosdbclient.rest.apirequests.save_metric_datapoints import SaveMetricDataPointsRequest, MetricDataPoints


class SaveMetricDataPointsRequestTest(unittest.TestCase):
    def test_save_metric_data_points_request(self):
        data_points = MetricDataPoints('metric', [[100, 5.4]], ttl=0, host='azure')
        request = SaveMetricDataPointsRequest(data_points=data_points)

        self.assertEqual(request.payload(), [{'name': 'metric',
                                              'tags': {'host': 'azure'},
                                              'datapoints': [[100, 5.4]]
                                             }])
        self.assertEqual(request.resource, None)
        self.assertEqual(request.success_status_code, 204)
        self.assertEqual(request.uri, 'datapoints')