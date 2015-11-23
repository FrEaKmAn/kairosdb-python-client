from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import TagNames


class QueryTagNamesRequest(Request):
    uri = 'tagnames'
    resource = TagNames
    success_status_code = 200

    def payload(self):
        return None