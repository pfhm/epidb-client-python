import urllib
import urllib2
import base64
from datetime import datetime, date

try:
    import simplejson as json
except ImportError:
    import json

__version__ = '0.1.5-alpha-3'
__user_agent__ = 'EpiDB-Client/%s (python)' % __version__

class InvalidResponseError(Exception):
    pass

class ResponseError(Exception):
    def __init__(self, code, msg, *args, **kwargs):
        self.code = code
        self.msg = msg
        Exception.__init__(self, *args, **kwargs)

class BasicClient:
    version = __version__
    user_agent = __user_agent__

    def _send(self, url, method='GET', param={}, headers={}, cookies={}):
        data = None
        if param:
            data = urllib.urlencode(param)

        if method == 'POST' and data is None:
            data = ''

        req = urllib2.Request(url)

        for header in headers:
            req.add_header(header, headers[header])

        if cookies:
            req.add_header('Cookie', urllib.urlencode(cookies))

        req.add_header('User-Agent', self.user_agent)

        sock = urllib2.urlopen(req, data)
        res = sock.read()
        sock.close()

        return res

    def _call(self, url, method='GET', param={}, headers={}, cookies={}):
        res = None
        err = None

        try:
            res = self._send(url, method, param, headers, cookies)
        except urllib2.HTTPError, e:
            err = e
            res = e.read()

        try:
            data = json.loads(res)
            if err is not None:
                if data.get('stat', None) != 'fail' or \
                        data.get('code', None) is None or \
                        data.get('msg', None) is None:
                    raise InvalidResponseError()
                raise ResponseError(int(data['code']), data['msg'])
            if data.get('stat', None) != 'ok':
                raise InvalidResponseError()
            return data
        except ValueError:
            if err is not None:
                raise err
            raise InvalidResponseError()

    def _encode_auth(self, key):
        return base64.encodestring('%s:%s' % (key, key)).replace("\n", "")

    def _auth_call(self, url, api_key, method='GET', param={}, headers={}, 
                   cookies={}):
        headers['Authorization'] = 'Basic %s' % self._encode_auth(api_key)
        return self._call(url, method, param, headers, cookies)

    def _admin_call(self, url, session_id, method='GET', param={}, headers={},
                    cookies={}):
        cookies['session_id'] = session_id
        return self._call(url, method, param, headers, cookies)

class DateEncoder(json.JSONEncoder):
    """Encode dates and datetimes as iso format."""
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

class EpiDBClient(BasicClient):
    server = 'https://egg.science.uva.nl:7443'
    path_response = '/response/'
    path_profile = '/profile/'

    _date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, api_key=None):
        self.api_key = api_key

    def _get_server(self):
        return self.server.strip().rstrip(' /')

    def _format_date(self, date):
        """Klaas says: Note that dates are sent as 2000-01-01 12:23:33 as opposed to our standard
        Isoformat. This is for historical reasons: I don't dare to change it yet."""

        if date is None:
            date = datetime.utcnow()
        return date.strftime(self._date_format)

    def response_submit(self, user_id, survey_id, answers, date=None):
        date = self._format_date(date)
        param = {
            'user_id': user_id,
            'survey_id': survey_id,
            'date': date,
            'answers': json.dumps(answers, cls=DateEncoder)
        }

        url = self._get_server() + self.path_response
        res = self._auth_call(url, self.api_key, method='POST', param=param)

        return res

    def profile_update(self, user_id, survey_id, answers, date=None):
        date = self._format_date(date)
        param = {
            'survey_id': survey_id,
            'date': date,
            'answers': json.dumps(answers, cls=DateEncoder)
        }

        url = self._get_server() + self.path_profile + user_id + '/'
        res = self._auth_call(url, self.api_key, method='POST', param=param)

        return res

# vim: set ts=4 sts=4 expandtab:
