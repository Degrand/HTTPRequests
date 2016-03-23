"""
    This module handles basic HTTP message contents.

"""

import datetime
from HTTPRequests.cookie import Cookie

class HttpRequestMessage(object):

    """ Object to encapsulate the concept of an HTTP Request """

    def __init__(self, method, page, dst, headers, **kwargs):

        self.method = method.upper()
        self.page = page
        self.dst = dst
        self.cookies = self.verify_cookies(kwargs.get('cookies', {}))
        self.body = kwargs.get('body', "")
        self.http_ver = kwargs.get('http_version', '1.1')
        self.headers = self.create_headers(headers)
        self.message = self.create_message()

    def __str__(self):

        return self.message

    def create_message(self):

        """ Create message, header and body, then assemble for HTTP Request """
        request = self.create_request()
        headers = self.create_header_str()
        data = self.body
        return "%s%s\r\n%s" % (request, headers, data)

    def create_request(self):

        """ Create request line for resource """
        params = (self.method, self.page, self.http_ver)
        return "%s %s HTTP/%s\r\n" % (params)

    def create_headers(self, headers=None):

        """ Create common HTTP requests headers """
        header_vals = [('connection', 'keep-alive'),
                       ('host', self.dst),
                       ('from', 'bot@no.com'),
                       ('user-agent', 'RequestBot_0.1'),
                       ('cookie', self.create_cookie_header())]

        if self.method == "POST":
            header_vals.extend(self.create_post_headers())

        elif self.method == "GET":
            header_vals.extend(self.create_get_headers())

        return self.merge_header_vals(header_vals, headers)

    def create_header_str(self):

        """ Convert header dictionary into valid HTTP Headers """
        retlist = ["%s: %s\r\n" % (k, v) for k, v in self.headers.items()]
        return ''.join(retlist)

    def create_post_headers(self):

        """ Create POST specific HTTP request headers """
        header_vals = [('content-type', 'application/x-www-form-urlencoded'),
                       ('content-length', len(self.body)),
                       ('accept', '*/*')]

        return header_vals

    def create_get_headers(self):

        """ Create GET specific HTTP request headers """
        header_vals = [('accept', 'text/html, text/plain'),
                       ('date', get_datetime())]

        return header_vals

    def merge_header_vals(self, header_vals, headers):

        """ Convert tuple list into key: value pairs for header dict """
        #NOTE: Possible collisions if value assigned twice with varying case
        if not headers:
            headers = {}
        std_dict = {k.title(): v for k, v in headers.items()}
        for k, v in header_vals:
            if v and k.title() not in std_dict:
                std_dict[k.title()] = v
        return std_dict

    def verify_cookies(self, cookies):

        """ Verify validity of provided cookies """
        if cookies is None:
            cookies = {}
        if isinstance(cookies, Cookie):
            cookies = {"cookie": cookies}
        return {k: v for k, v in cookies.items() if v != None}

    def create_cookie_header(self):

        """ Create values for HTTP Cookie header """
        if self.cookies is None:
            self.cookies = {}
        if isinstance(self.cookies, Cookie):
            self.cookies = {"Cookie": self.cookies}
        retlist = []
        for k, v in self.cookies.items():
            if isinstance(v, Cookie):
                retlist.append(str(v))
            else:
                retlist.append("%s=%s;" % (k, v))
        return ' '.join(retlist)

class HttpResponseMessage(object):

    """ Object to encapsulate the concept of an HTTP Response """
    def __init__(self, response, headers, body):

        #NOTE: This should handle raw input from server
        self.response = response
        self.headers = headers
        self.cookies = self.set_cookies()
        self.body = body
        self.status_code, self.status_msg = self.parse_response()

    def __str__(self):

        return self.body

    def get_status_code(self):

        """ Return 3 digit status code of HTTP response """
        return self.status_code

    def parse_response(self):

        """ Return status code and status message """
        resplist = self.response.split(' ')
        return int(resplist[1]), resplist[2]

    def set_cookies(self):

        """ Check for cookies in response headers """
        cookies = {}
        if "Set-Cookie" in self.headers:
            cookielist = self.headers["Set-Cookie"].split(',')
            if not isinstance(cookielist, list):
                cookielist = [cookielist]
            for cookie in cookielist:
                fields = cookie.split(';')
                delim = fields[0].find('=')
                name, val = fields[0][:delim], fields[0][delim+1:]
                # path should NOT be hardcoded
                path, domain = '/', self.headers.get('Host')
                args = {'Raw-String': cookie}
                for elem in fields[1:]:
                    if '=' in elem:
                        k, v = elem.split('=')
                        args[k] = v
                    elif elem.lower() == "secure":
                        args['Secure'] = True
                    elif elem.lower() == "httponly":
                        args['HttpOnly'] = True
                cookies[name] = Cookie(name, val, domain, path, **args)
        return cookies

def get_datetime(dt=None):

    """ Get current datetime in standardized format """
    if not dt:
        dt = datetime.datetime.utcnow()
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
