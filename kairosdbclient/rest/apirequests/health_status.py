from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import HealthStatus


class HealthStatusRequest(Request):
    uri = 'health/status'
    resource = HealthStatus
    success_status_code = 200
    request_method = 'GET'

    def payload(self):
        return None