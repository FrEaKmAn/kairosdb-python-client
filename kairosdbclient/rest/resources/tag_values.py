from kairosdbclient.rest.resources.base import Resource


class TagValues(Resource):
    def __init__(self, request, response):
        super(TagValues, self).__init__(request)
        self.values = response.json()['results']