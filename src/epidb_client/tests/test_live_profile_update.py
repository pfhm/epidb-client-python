import unittest

import epidb_client
from epidb_client import EpiDBClient
from epidb_client.tests import config

class LiveProfileUpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.client = EpiDBClient(config.api_key)
        self.client.server = config.server

        self.data = {'user_id': config.user_id,
                     'p0000': '0',
                     'p0001': '1',
                     'p0002': '2'}

    def testSuccess(self):
        result = self.client.profile_update(config.user_id, 
                                            config.profile_survey_id, 
                                            self.data)
        self.assertEqual(result['stat'], 'ok')

class LiveProfileUpdateUnauthorizedTestCase(unittest.TestCase):
    def setUp(self):
        self.client = EpiDBClient(config.api_key_invalid)
        self.client.server = config.server

        self.data = {'user_id': config.user_id,
                     'p0000': '0',
                     'p0001': '1',
                     'p0002': '2'}

    def testUnauthorized(self):
        try:
            self.client.profile_update(config.user_id, 
                                       config.profile_survey_id, 
                                       self.data)
            self.fail()
        except epidb_client.ResponseError, e:
            self.assertEqual(e.code, 401)

if __name__ == '__main__':
    unittest.main()

# vim: set ts=4 sts=4 expandtab:

