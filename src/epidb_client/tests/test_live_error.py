import unittest
import urllib2
import random
import socket

from epidb_client import EpiDBClient
from epidb_client.tests import config

class LiveErrorsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = EpiDBClient(config.api_key)

        self.data = {'user_id': config.user_id,
                     'p0000': '0',
                     'p0001': '1',
                     'p0002': '2'}

    def testInvalidHost(self):
        self.client.server = 'http://localhost.example/'
        try:
            self.client.profile_update(config.user_id,
                                       config.profile_survey_id, 
                                       self.data)
            self.fail()
        except urllib2.URLError, e:
            self.assertEqual(e.reason.errno, 8)

    def _get_close_port(self):
        while True:
            port = int(random.random() * 35000)
            ss = socket.socket()
            ss.settimeout(0.25)
            try:
                ss.connect(('127.0.0.1', port))
                ss.close()
            except socket.error:
                return port

    def testConnectionRefused(self):
        port = self._get_close_port()

        self.client.server = 'http://127.0.0.1:%d/' % port
        try:
            self.client.profile_update(config.user_id,
                                       config.profile_survey_id, 
                                       self.data)
            self.fail()
        except urllib2.URLError, e:
            self.assertEqual(e.reason.errno, 61)

if __name__ == '__main__':
    unittest.main()

# vim: set ts=4 sts=4 expandtab:

