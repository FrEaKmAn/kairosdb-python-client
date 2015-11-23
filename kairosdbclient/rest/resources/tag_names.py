from kairosdbclient.rest.resources.base import Resource


class TagNames(Resource):
    def __init__(self, response):
        self.names = response.json()['results']