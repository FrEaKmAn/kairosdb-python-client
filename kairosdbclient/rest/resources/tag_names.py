from kairosdbclient.rest.resources.base import Resource


class TagNames(Resource):
    def __init__(self, request, response):
        super(TagNames, self).__init__(request)
        self.names = response.json()['results']