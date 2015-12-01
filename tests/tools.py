import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_resource_as_json(filename):
    return json.loads(get_resource(filename))


def get_resource(filename):
    with open(os.path.join(BASE_DIR, 'tests/resources', filename)) as resource_file:
        return resource_file.read()


class MockResponse(object):
    def __init__(self, json_content=None, status_code=None, text=None):
        self._json = json_content
        self._status_code = status_code
        self._text = text

    def json(self):
        if isinstance(self._json, str):
            return json.loads(self._json)

        return self._json

    @property
    def status_code(self):
        return self._status_code

    @property
    def text(self):
        return self._text


class MockAPIRequest(object):
    def __init__(self, success_status_code):
        self._success_status_code = success_status_code

    @property
    def success_status_code(self):
        return self._success_status_code

    def to_resource(self, response):
        pass