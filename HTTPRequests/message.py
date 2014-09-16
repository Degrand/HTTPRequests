import datetime

class HttpRequestMessage(object):

    """ Object to encapsulate the concept of an HTTP Request """

    def __init__(self, action, page, dest, headers, body="", http_ver=1.1):

        self.action = action.upper()
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
        params = (self.action, self.page, self.http_ver)
        return "%s %s HTTP/%s\r\n" % (params)

    def create_headers(self):

        """ Create common HTTP requests headers """
        if self.headers is None:
            self.headers = {}
        header_vals = [('connection', 'keep-alive'),
                       ('host', self.dest),
                       ('from', 'bot@no.com'),
                       ('user-agent', 'RequestBot_0.1')]

        if self.action == "POST":
            header_vals.extend(self.set_POST_headers())

        elif self.action == "GET":
            header_vals.extend(self.set_GET_headers())

        self.set_header_vals(header_vals)
        return self.create_header_str()

    def create_header_str(self):

        """ Convert header dictionary into valid HTTP Headers """
        retlist = ["%s: %s\r\n" % (k, v) for k, v in self.headers.iteritems()]
        return ''.join(retlist)

    def set_POST_headers(self):

        """ Create POST specific HTTP request headers """
        header_vals = [('content-type', 'application/x-www-form-urlencoded'),
                       ('content-length', len(self.body)),
                       ('accept', '*/*')]

        return header_vals

    def set_GET_headers(self):

        """ Create GET specific HTTP request headers """
        header_vals = [('accept', 'text/html, text/plain'),
                       ('date', get_datetime())]

        return header_vals

    def set_header_vals(self, header_vals):

        """ Convert tuple list into key: value pairs for header dict """
        #NOTE: Possible collisions if value assigned twice with varying case
        std_dict = {k.title(): v for k, v in self.headers.iteritems()}
        for k, v in header_vals:
            std_dict.set_default(k.title(), v)
        self.headers = std_dict

class HttpResponseMessage(object):

    """ Object to encapsulate the concept of an HTTP Response """
    def __init__(self, response, headers, body):

        #NOTE: This should handle raw input from server
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

    """ Get current datetime in standardized format """
    if not dt:
        dt = datetime.datetime.utcnow()
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
