from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import MetricDataPoints


class QueryMetricDataPointsRequest(Request):
    uri = 'datapoints/query'
    resource = MetricDataPoints
    success_status_code = 200

    def __init__(self, start, end, metrics, time_zone=None, cache_time=0):
        super(QueryMetricDataPointsRequest, self).__init__()

        self.start = start
        self.end = end
        self.time_zone = time_zone
        self.cache_time = cache_time
        self.metrics = metrics

    def payload(self):
        payload = dict(self._format_time('start', self.start).items() + self._format_time('end', self.end).items())
        payload['metrics'] = map(lambda m: m.format(), self.metrics)
        return payload

