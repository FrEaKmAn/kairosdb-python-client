from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import MetricTags


class QueryMetricTagsRequest(Request):
    uri = 'datapoints/query/tags'
    resource = MetricTags
    success_status_code = 200

    def __init__(self, start, end, metrics):
        super(QueryMetricTagsRequest, self).__init__()

        self._start = start
        self._end = end
        self._metrics = metrics

    def payload(self):
        start = self.format_time('start', self._start)
        end = self.format_time('end', self._end)
        metrics = self.format_metrics(self._metrics)

        return {
            'start': start,
            'end': end,
            'metrics': metrics
        }

    def format_metrics(self, metrics):
        if type(metrics) is list or type(metrics) is tuple:
            return {"metrics": [{'name': metric} for metric in metrics]}

        return metrics
