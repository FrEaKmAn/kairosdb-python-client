from kairosdbclient.rest.apirequests.base import Request


class DeleteMetricRequest(Request):
    resource = None
    success_status_code = 204

    def __init__(self, name):
        self.name = name
        super(DeleteMetricRequest, self).__init__()

    def payload(self):
        return None

    @property
    def uri(self):
        return 'metric/%s' % self.name