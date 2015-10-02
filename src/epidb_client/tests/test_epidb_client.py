import unittest
import urllib
import base64
from datetime import datetime

try:
    import simplejson as json
except ImportError:
    import json

import epidb_client
from epidb_client import BasicClient
from epidb_client.tests import config
from epidb_client.tests.mocks import *

class TestCase(unittest.TestCase):
    def setUp(self):
        self.urllib2 = MockUrllib2()
        self.urllib2_orig = epidb_client.urllib2
        epidb_client.urllib2 = self.urllib2

        self.client = epidb_client.EpiDBClient(config.api_key)
        self.client.server = config.server

    def tearDown(self):
        epidb_client.urllib2 = self.urllib2_orig 

class EpiDbClientTestCase(TestCase):
    def testApiKey(self):
        self.assertEqual(self.client.api_key, config.api_key)

    def testResponseSubmitCall(self):
        eresult = {'stat': 'ok',
                   'id': '00000000-0000-0000-0000-000000000000'}
        dresult = json.dumps(eresult)
        self.urllib2._result = dresult

        answers = {'name': 'john doe',
                   'address': 'amsterdam',
                   'plus_sign': '1 + 1',
                   'ampersand': '1 & 1'}

        res = self.client.response_submit(config.user_id, config.survey_id,
                                          answers)

        # Make sure the result is the same
        self.assertEqual(res, eresult)

        # Check sent data
        values = self.urllib2.data.split('&')

        keys = map(lambda x: x.split('=')[0], values)
        self.assertEqual(sorted(keys), sorted(['user_id', 'survey_id', 
                                               'answers', 'date']))
        
        param = {}
        for value in values:
            (key, val) = value.split('=')
            val = val.replace('+', ' ')
            val = urllib.unquote(val)
            param[key] = val

        self.assertEqual(param['user_id'], config.user_id)
        self.assertEqual(param['survey_id'], config.survey_id)

        ans = json.loads(param['answers'])
        self.assertEqual(ans, answers)

        datetime.strptime(param['date'], '%Y-%m-%d %H:%M:%S')

        # Check API Key
        self.assertTrue('Authorization' in self.urllib2.request.headers)
        auth = self.urllib2.request.headers['Authorization']
        (auth_type, auth_string) = auth.split(' ', 1)

        self.assertEqual(auth_type, 'Basic')

        decoded = base64.decodestring(auth_string)
        (key1, key2) = decoded.split(':', 1)

        self.assertEqual(key1, key2)
        self.assertEqual(key1, config.api_key)

        # Check URL
        self.assertEqual("%sresponse/" % config.server, 
                         self.urllib2.request.url)

    def testResponseSubmitCallDate(self):
        eresult = {'stat': 'ok',
                   'id': '00000000-0000-0000-0000-000000000000'}
        dresult = json.dumps(eresult)
        self.urllib2._result = dresult

        date = datetime(2009, 12, 16, 1, 2, 3)
        answers = {}

        res = self.client.response_submit(config.user_id, config.survey_id,
                                          answers, date)

        values = self.urllib2.data.split('&')

        (key, val) = filter(lambda x: x.split('=')[0] == 'date', 
                            values)[0].split('=')

        val = val.replace('+', ' ')
        val = urllib.unquote(val)
        self.assertEqual(val, '2009-12-16 01:02:03')

    def testUpdateProfileCall(self):
        eresult = {'stat': 'ok',
                   'id': '00000000-0000-0000-0000-000000000000'}
        dresult = json.dumps(eresult)
        self.urllib2._result = dresult

        answers = {'name': 'john doe',
                   'address': 'amsterdam',
                   'plus_sign': '1 + 1',
                   'ampersand': '1 & 1'}

        res = self.client.profile_update(config.user_id, 
                                         config.profile_survey_id,
                                         answers)

        # Make sure the result is the same
        self.assertEqual(res, eresult)

        # Check sent data
        values = self.urllib2.data.split('&')

        keys = map(lambda x: x.split('=')[0], values)
        self.assertEqual(sorted(keys), sorted(['survey_id', 
                                               'answers', 'date']))
        
        param = {}
        for value in values:
            (key, val) = value.split('=')
            val = val.replace('+', ' ')
            val = urllib.unquote(val)
            param[key] = val

        self.assertEqual(param['survey_id'], config.profile_survey_id)

        ans = json.loads(param['answers'])
        self.assertEqual(ans, answers)

        datetime.strptime(param['date'], '%Y-%m-%d %H:%M:%S')

        # Check API Key
        self.assertTrue('Authorization' in self.urllib2.request.headers)
        auth = self.urllib2.request.headers['Authorization']
        (auth_type, auth_string) = auth.split(' ', 1)

        self.assertEqual(auth_type, 'Basic')

        decoded = base64.decodestring(auth_string)
        (key1, key2) = decoded.split(':', 1)

        self.assertEqual(key1, key2)
        self.assertEqual(key1, config.api_key)

        # Check URL
        self.assertEqual("%sprofile/%s/" % (config.server, config.user_id), 
                         self.urllib2.request.url)

    def testProfileUpdateCallDate(self):
        eresult = {'stat': 'ok',
                   'id': '00000000-0000-0000-0000-000000000000'}
        dresult = json.dumps(eresult)
        self.urllib2._result = dresult

        date = datetime(2009, 12, 16, 1, 2, 3)
        answers = {}

        res = self.client.profile_update(config.user_id, config.survey_id,
                                         answers, date)

        values = self.urllib2.data.split('&')

        (key, val) = filter(lambda x: x.split('=')[0] == 'date', 
                            values)[0].split('=')

        val = val.replace('+', ' ')
        val = urllib.unquote(val)
        self.assertEqual(val, '2009-12-16 01:02:03')


class URLTestCase(TestCase):
    def testURL(self):
        eresult = '{"stat": "ok"}'
        self.urllib2._result = eresult

        baseurl = "http://epiwork.eu"
        expected = "%s/response/" % baseurl

        self._test_url(expected, "http://epiwork.eu")
        self._test_url(expected, "http://epiwork.eu/")
        self._test_url(expected, "http://epiwork.eu//")
        self._test_url(expected, "http://epiwork.eu ")
        self._test_url(expected, "http://epiwork.eu  ")
        self._test_url(expected, "http://epiwork.eu /")
        self._test_url(expected, "http://epiwork.eu  /")
        self._test_url(expected, "http://epiwork.eu //")
        self._test_url(expected, " http://epiwork.eu //")

    def _test_url(self, expected, url):
        data = {}
        self.client.server = url
        res = self.client.response_submit(config.user_id, config.survey_id, 
                                          data)
        self.assertEqual(expected, self.urllib2.request.url)

if __name__ == '__main__':
    unittest.main()

