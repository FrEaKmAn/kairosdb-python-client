from kairosdbclient.rest.apirequests.save_metric_datapoints import MetricDataPoints
import requests
from kairosdbclient.exceptions import ResponseException

from kairosdbclient.rest.apirequests import *
from kairosdbclient.rest.metric import SingleMetric


class KairosDBRestClient(object):
    def __init__(self, host="http://127.0.0.1", port=8080):
        self.host = host
        self.port = port

    def _get_url(self, uri):
        return "%s:%s/api/v1/%s" % (self.host, self.port, uri)

    def _make_request(self, request):
        response = requests.request(request.request_method, self._get_url(request.uri), json=request.payload())
        return self._parse_response(request, response)

    def _parse_response(self, request, response):
        if response.status_code is not request.success_status_code:
            raise ResponseException(response.status_code, message=response.text)

        return request.to_resource(response)

    def version(self):
        return self._make_request(VersionRequest())

    def metric_tags(self, start, end, metrics):
        return self._make_request(QueryMetricTagsRequest(start, end, metrics))

    def metric_names(self):
        return self._make_request(QueryMetricNamesRequest())

    def tag_names(self):
        return self._make_request(QueryTagNamesRequest())

    def tag_values(self):
        return self._make_request(QueryTagValuesRequest())

    def delete_metric(self, name):
        return self._make_request(DeleteMetricRequest(name))

    def health_check(self):
        return self._make_request(HealthCheckRequest())

    def health_status(self):
        return self._make_request(HealthStatusRequest())

    def query(self, start, end, metrics, time_zone=None, cache_time=0):
        return self._make_request(QueryMetricDataPointsRequest(start, end, metrics, time_zone, cache_time))

    def save(self, data_points):
        return self._make_request(SaveMetricDataPointsRequest(data_points))

    def save_single(self, metric_name, data_points, tags=None, ttl=0, **kwargs):
        data_points = MetricDataPoints(metric_name, data_points, tags, ttl, **kwargs)
        return self.save(data_points)

    def delete(self, data_points):
        return self._make_request(DeleteMetricDataPointsRequest(data_points))

    def delete_single(self, metric_name, data_points, tags=None, **kwargs):
        data_points = MetricDataPoints(metric_name, data_points, tags, **kwargs)
        return self.delete(data_points)

    def __getitem__(self, item):
        time, metrics = item

        single_metric = SingleMetric(self.query, time.start, time.stop, metrics)
        if time.step:
            single_metric.aggregate(time.step)

        return single_metric