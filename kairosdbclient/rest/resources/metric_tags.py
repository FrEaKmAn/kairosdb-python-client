from kairosdbclient.rest.resources.base import Resource


class MetricTags(Resource):
    results = []

    def __init__(self, response):
        self.results = response.json()['results']