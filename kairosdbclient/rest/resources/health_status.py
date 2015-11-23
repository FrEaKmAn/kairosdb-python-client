from kairosdbclient.rest.resources.base import Resource


class HealthStatus(Resource):
    def __init__(self, response):
        self.messages = dict(map(lambda i: str(i).split(': '), response.json()))

    @property
    def jvm_thread_deadlock(self):
        return self.messages['JVM-Thread-Deadlock']

    @property
    def datastore_query(self):
        return self.messages['Datastore-Query']