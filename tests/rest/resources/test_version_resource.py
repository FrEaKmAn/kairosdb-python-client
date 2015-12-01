import unittest
from kairosdbclient.rest.resources.version import Version
from tests.tools import MockResponse, get_resource_as_json


class VersionResourceTest(unittest.TestCase):
    def setUp(self):
        response = MockResponse(json_content=get_resource_as_json('version.json'))
        self.resource = Version(response)

    def test_version(self):
        self.assertEqual(self.resource.version, 'KairosDB 0.9.4')

    def test_code(self):
        self.assertEqual(self.resource.code, '0.9.4')