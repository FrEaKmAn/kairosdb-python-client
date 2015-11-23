from kairosdbclient.rest.resources.base import Resource


class TagValues(Resource):
    def __init__(self, response):
        self.values = response.json()['results']