import unittest

import epidb_client
from epidb_client import EpiDBClient
from epidb_client.tests import config

class LiveResponseSubmitTestCase(unittest.TestCase):
    def setUp(self):
        self.client = EpiDBClient(config.api_key)
        self.client.server = config.server

        self.answers = {'q0000': '0',
                        'q0001': '1',
                        'q0002': '2'}

    def testSuccess(self):
        result = self.client.response_submit(config.user_id,
                                             config.survey_id,
                                             self.answers)
        self.assertEqual(result['stat'], 'ok')

class LiveResponseSubmitUnauthorizedTestCase(unittest.TestCase):
    def setUp(self):
        self.client = EpiDBClient(config.api_key_invalid)
        self.client.server = config.server

        self.answers = {'q0000': '0',
                        'q0001': '1',
                        'q0002': '2'}

    def testUnauthorized(self):
        try:
            self.client.response_submit(config.user_id,
                                        config.survey_id,
                                        self.answers)
            self.fail()
        except epidb_client.ResponseError, e:
            self.assertEqual(e.code, 401)

class GGMResponseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = EpiDBClient(config.api_key)
        self.client.server = config.server

        self.answers = {'a20000': '0',
                        'a21000': '2009-12-15',}

    def testSuccess(self):
        result = self.client.response_submit(config.user_id,
                                             'dev-response-nl-0.0',
                                             self.answers)
        self.assertEqual(result['stat'], 'ok')

if __name__ == '__main__':
    unittest.main()

# vim: set ts=4 sts=4 expandtab:

