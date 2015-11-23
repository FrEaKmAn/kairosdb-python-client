from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import MetricDataPoints


class QueryMetricDataPointsRequest(Request):
    uri = 'datapoints/query'
    resource = MetricDataPoints
    success_status_code = 200

    def __init__(self, start, end, metrics):
        super(QueryMetricDataPointsRequest, self).__init__()

        self.start = start
        self.end = end
        self.metrics = metrics

    def payload(self):
        payload = dict(self.format_time('start', self.start).items() + self.format_time('end', self.end).items())
        payload['metrics'] = [self.format_metric(metric) for metric in self.metrics]
        return payload

    def format_metric(self, metric):
        request = {
            'name': metric.name,
        }

        if metric.tags:
            request['tags'] = metric.tags

        if metric.limit:
            request['limit'] = metric.limit

        if metric.group_bys:
            request['group_by'] = metric.group_bys

        if metric.aggregators:
            request['aggregators'] = metric.aggregators

        return request