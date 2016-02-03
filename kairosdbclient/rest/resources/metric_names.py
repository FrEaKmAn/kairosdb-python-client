from kairosdbclient.rest.resources.base import Resource


class MetricNames(Resource):
    def __init__(self, request, response):
        super(MetricNames, self).__init__(request)
        self.names = response.json()['results']