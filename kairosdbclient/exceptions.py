class RequestException(Exception):
    pass


class ResponseException(Exception):
    def __init__(self, status_code, *args, **kwargs):
        super(Exception, self).__init__(args, kwargs)
        self.status_code = status_code