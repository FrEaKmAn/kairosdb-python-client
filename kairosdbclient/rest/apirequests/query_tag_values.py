from kairosdbclient.rest.apirequests.base import Request
from kairosdbclient.rest.resources import TagValues


class QueryTagValuesRequest(Request):
    uri = 'tagvalues'
    resource = TagValues
    success_status_code = 200

    def payload(self):
        return None