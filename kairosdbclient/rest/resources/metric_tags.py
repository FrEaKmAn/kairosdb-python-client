from kairosdbclient.rest.resources.base import Resource


class MetricTags(Resource):
    def __init__(self, request, response):
        super(MetricTags, self).__init__(request)
        self.results = response.json()['results']