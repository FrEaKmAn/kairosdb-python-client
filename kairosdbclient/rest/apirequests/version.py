from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import Version


class VersionRequest(Request):
    uri = 'version'
    resource = Version
    success_status_code = 200
    request_method = 'GET'

    def payload(self):
        return None