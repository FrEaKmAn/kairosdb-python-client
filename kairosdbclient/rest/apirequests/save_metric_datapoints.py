from kairosdbclient.rest.apirequests.base import Request


class SaveMetricDataPointsRequest(Request):
    uri = 'datapoints'
    resource = None
    success_status_code = 204
    request_method = 'POST'

    def __init__(self, data_points):
        super(SaveMetricDataPointsRequest, self).__init__()

        if not isinstance(data_points, (list, tuple)):
            data_points = [data_points]

        self._data_points = data_points

    def payload(self):
        return [data_point.format() for data_point in self._data_points]


class MetricDataPoints(object):
    def __init__(self, name, data_points, tags=None, ttl=0, **kwargs):
        self._name = name
        self._data_points = data_points
        self._tags = {}
        self._ttl = ttl

        self._parse_tags(tags, **kwargs)

    def _parse_tags(self, tags, **kwargs):
        if tags:
            self._tags.update(tags)

        if kwargs:
            self._tags.update(**kwargs)

    def format(self):
        request = {
            'name': self._name,
            'datapoints': self._data_points,
            'tags': self._tags,
        }

        if self._ttl:
            request['ttl'] = self._ttl

        return request