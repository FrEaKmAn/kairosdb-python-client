class ClientException(Exception):
    pass


class RequestException(ClientException):
    pass


class ResponseException(ClientException):
    def __init__(self, status_code, *args, **kwargs):
        super(Exception, self).__init__(args, kwargs)
        self.status_code = status_code


class MetricException(ClientException):
    pass


class AggregatorException(ClientException):
    pass


class GroupByException(ClientException):
    pass