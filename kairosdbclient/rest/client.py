import requests
from kairosdbclient.exceptions import ResponseException

from kairosdbclient.rest.apirequests import *
from kairosdbclient.rest.query import SingleMetric


class KairosDBRestClient(object):
    def __init__(self, host="http://127.0.0.1", port=8080):
        self.host = host
        self.port = port

    def get_url(self, uri):
        return "%s:%s/api/v1/%s" % (self.host, self.port, uri)

    def _make_request(self, method, request):
        response = requests.request(method, self.get_url(request.uri), json=request.payload())
        return self._parse_response(request, response)

    def _parse_response(self, request, response):
        if response.status_code is not request.success_status_code:
            raise ResponseException(response.status_code, message=response.text)

        return request.to_resource(response)

    def version(self):
        return self._make_request('GET', VersionRequest())

    def metric_tags(self, start, end, metrics):
        return self._make_request('POST', QueryMetricTagsRequest(start, end, metrics))

    def metric_names(self):
        return self._make_request('GET', QueryMetricNamesRequest())

    def tag_names(self):
        return self._make_request('GET', QueryTagNamesRequest())

    def tag_values(self):
        return self._make_request('GET', QueryTagValuesRequest())

    def delete_metric(self, name):
        return self._make_request('DELETE', DeleteMetricRequest(name))

    def health_check(self):
        return self._make_request('GET', HealthCheckRequest())

    def health_status(self):
        return self._make_request('GET', HealthStatusRequest())

    def query(self, start, end, metrics):
        return self._make_request('POST', QueryMetricDataPointsRequest(start, end, metrics))

    def __getitem__(self, item):
        time, metrics = item
        return SingleMetric(self.query, time.start, time.stop, metrics)