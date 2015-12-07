from kairosdbclient.rest.apirequests.base import Request


class HealthCheckRequest(Request):
    uri = 'health/check'
    resource = None
    success_status_code = 204
    request_method = 'GET'

    def payload(self):
        return None