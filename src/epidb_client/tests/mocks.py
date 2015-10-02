
class MockRequest:
    def __init__(self, url):
        self.url = url
        self.headers = {}

    def add_header(self, field, value):
        self.headers[field] = value

class MockSock:
    def __init__(self, result):
        self._result = result
        self.closed = False

    def read(self):
        return self._result

    def close(self):
        self.closed = True

class MockUrllib2:
    Request = MockRequest

    _result = None
    _error = None

    def __init__(self):
        self._reset()

    def _reset(self):
        self.request = None
        self.data = None
        self._error = None

    def urlopen(self, request, data):
        self.request = request
        self.data = data

        if self._error is not None:
            if type(self._error).__name__ == 'str':
                raise self.HTTPError(self._error)
            else:
                raise self._error
        else:
            return MockSock(self._result)

    class HTTPError:
        def __init__(self, msg):
            self._msg = msg

        def read(self):
            return self._msg

