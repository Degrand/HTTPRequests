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
            std_dict.setdefault(k.title(), v)
        self.headers = std_dict

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

        return self.response+" "+'\n'.join([k for k in self.headers])

    def get_status_code(self):

        """ Return 3 digit status code of HTTP response """
        return self.status_code

    def parse_response(self):

        """ Return status code and status message """
        resplist = self.response.split(' ')
        return int(resplist[1]), resplist[2]

    def set_cookies(self):

        """ Check for cookies in response headers """
        if "Set-Cookie" in self.headers:
            cookies = {}
            cookielist = self.headers["Set-Cookie"].split(',')
            if not isinstance(cookielist, list):
                cookielist = [cookielist]
            for cookie in cookielist:
                fields = cookie.split(';')
                name, val = fields[0].split('=')
                path, domain = '/', self.headers.get('Host')
                args = {}
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
            
class Cookie(object):

    """ Encapsulates the values of an HTTP Cookie """
    def __init__(self, name, value, domain, path, **kwargs):
        self.name = name
        self.value = value
        self.path = path
        self.domain = domain
        self.expires = kwargs.get('Expires')
        self.max_age = kwargs.get('Max-Age')
        self.secure = kwargs.get('Secure', False)
        self.httponly = kwargs.get('HttpOnly', False)
        self.cookie_str = self.set_cookie_str()

    def __str__(self):
        
        return self.cookie_str

    def __setattr__(self, name, value):
        
        """ Update value and rebuild cookie_str to match """
        object.__setattr__(self, name, value)
        if "cookie_str" in self.__dict__ and name != "cookie_str": 
            #conditional avoids conflict with init assignment
            self.cookie_str = self.set_cookie_str()

    def set_cookie_str(self):

        """ Creates HTTP valid cookie string """
        retstring = "%s=%s; Path=%s;" % (self.name, self.value,
                                                    self.path)
        if self.domain:
            retstring += " Domain=%s;" % self.domain
        if self.expires:
            retstring += " Expires=%s;" % self.expires
        if self.max_age:
            retstring += " Max-Age=%s;" % self.max_age
        if self.secure:
            retstring += " Secure;"
        if self.httponly:
            retstring += " HttpOnly;"
        return retstring

def get_datetime(dt=None):

    """ Get current datetime in standardized format """
    if not dt:
        dt = datetime.datetime.utcnow()
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
