from abc import abstractmethod
from kairosdbclient.exceptions import RequestException


class Request(object):
    def __init__(self):
        if not hasattr(self, 'uri'):
            raise RequestException("Request %s needs to have uri attribute" % self.__class__.__name__)

        if not hasattr(self, 'resource'):
            raise RequestException("Request %s needs to have resource attribute" % self.__class__.__name__)

        if not hasattr(self, 'success_status_code'):
            raise RequestException("Request %s needs to have success_status_code attribute" % self.__class__.__name__)

    @abstractmethod
    def payload(self):
        pass

    def to_resource(self, response):
        resource = getattr(self, 'resource')
        return resource(response) if resource and response.status_code is not 204 else None

    def format_time(self, prefix, time):
        if isinstance(time, int):
            return {prefix + '_absolute': time}

        if isinstance(time, (list, tuple)):
            value, unit = time
            return {prefix + '_relative': {
                'value': value,
                'unit': unit
            }}

        return RequestException("Invalid time format %s" % time)