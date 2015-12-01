import unittest
from kairosdbclient.rest.apirequests.version import VersionRequest
from kairosdbclient.rest.resources.version import Version


class VersionRequestTest(unittest.TestCase):
    def test_version_request(self):
        request = VersionRequest()

        self.assertEqual(request.payload(), None)
        self.assertEqual(request.resource, Version)
        self.assertEqual(request.success_status_code, 200)
        self.assertEqual(request.uri, 'version')