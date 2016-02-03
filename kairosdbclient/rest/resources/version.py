from kairosdbclient.rest.resources.base import Resource


class Version(Resource):
    def __init__(self, request, response):
        super(Version, self).__init__(request)
        json = response.json()
        self.version = json['version']

    @property
    def code(self):
        return self.version.replace("KairosDB ", "")

    def __str__(self):
        return self.version