import datetime

class HttpRequestMessage(object):

    """ Object to encapsulate the concept of an HTTP Request """

    def __init__(self, action, page, dest, headers={}, body="", http_ver=1.1):

        self.action = action
        self.page = page
        self.dest = dest
        self.headers = headers
        self.body = body
        self.http_ver = http_ver
        self.message = self.create_message()

    def __str__(self):

        return self.message

    def create_message(self):

        """ Create message, header and body, then assemble for HTTP Request """
        request = self.create_request()
        headers = self.create_headers()
        data = self.body
        return "%s%s\r\n%s" % (request, headers, data)

    def create_request(self):

        """ Create request line for resource """
        params = (self.action.upper(), self.page, self.http_ver)
        return "%s %s HTTP/%s\r\n" % (params)

    def create_headers(self):

        """ Create common HTTP requests headers """
        date = self.headers.get('date', get_datetime())
        conn = self.headers.get('conn', 'keep-alive')
        host = self.headers.get('host', self.dest)
        from_ = self.headers.get('from', 'bot@no.com')
        accept = self.headers.get('accept', 'text/html, text/plain')
        user_agent = self.headers.get('user-agent', 'RequestBot_0.1')
        
        headers = ("Host: %s\r\n"
                   "Connection: %s\r\n"
                   "Date: %s\r\n"
                   "From: %s\r\n"
                   "Accept: %s\r\n"
                   "User-Agent: %s\r\n") % (host, conn, date, from_, 
                                             accept, user_agent)
        return headers

class HttpResponseMessage(object):

    """ Object to encapsulate the concept of an HTTP Response """
    def __init__(self, response, headers, body):

        """ NOTE: This should handle raw input from server """
        self.response = response
        self.headers = headers
        self.body = body
        self.status_code, self.status_msg = self.parse_response()

    def __str__(self):

        return self.response+" "+'\n'.join([k for k in self.headers])

    def get_status_code(self):

        """ Return 3 digit status code of HTTP response """
        return self.status_code

    def parse_response(self):

        """ Return status code and status message """
        resplist = self.response.split(' ')
        return int(resplist[1]), resplist[2]

def get_datetime(dt=None):

    if not dt:
        dt = datetime.datetime.utcnow()
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
