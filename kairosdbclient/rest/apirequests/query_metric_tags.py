from kairosdbclient.exceptions import RequestException
from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import MetricTags


class QueryMetricTagsRequest(Request):
    uri = 'datapoints/query/tags'
    resource = MetricTags
    success_status_code = 200
    request_method = 'POST'

    def __init__(self, start, end, metrics):
        super(QueryMetricTagsRequest, self).__init__()

        self._start = start
        self._end = end
        self._parse_metrics(metrics)

    def payload(self):
        request = {
            'metrics': map(lambda m: m.format(), self._metrics)
        }

        start = self._format_time('start', self._start)
        request.update(start)

        if self._end:
            end = self._format_time('end', self._end)
            request.update(end)

        return request

    def _parse_metrics(self, metrics):
        self._metrics = []

        for metric in metrics:
            if isinstance(metric, MetricTag):
                self._metrics.append(metric)
            elif isinstance(metric, dict):
                if 'name' not in metric:
                    raise RequestException("Missing name in metric: %s." % metric)

                name = metric['name']
                tags = metric.pop('tags', {})

                self._metrics.append(MetricTag(name, **tags))
            else:
                raise RequestException("Invalid metric type: %s, must be MetricTag or dict." % type(metric))


class MetricTag(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.tags = {}

        for name, tags in kwargs.items():
            if not isinstance(tags, (list, tuple)):
                tags = [tags]

            self.tags[name] = tags

    def format(self):
        request = {
            'name': self.name,
        }

        if self.tags:
            request['tags'] = self.tags

        return request