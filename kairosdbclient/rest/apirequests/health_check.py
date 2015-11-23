from kairosdbclient.rest.apirequests.base import Request


class HealthCheckRequest(Request):
    uri = 'health/check'
    resource = None
    success_status_code = 204

    def payload(self):
        return None