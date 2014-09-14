"""
    This module handles HTTP requests. It currently only supports basic
    GET and POST behavior

"""

import sys

from HTTPRequests.connection import WebSocket
from HTTPRequests.message import HttpRequestMessage, HttpResponseMessage

class HttpRequest(object):

    """ HTTP Request to server for some resource """

    def __init__(self, host):

        self.host = host
        self.port = self.check_port()
        self.request = None
        self.response = None
        self.redirect_count = 0

    def get(self, page='/', headers=None):

        """ Perform a GET request to host """
        self.request = HttpRequestMessage('GET', page, self.host, headers)
        self.do_request()

    def post(self, page='/', headers=None, data=""):

        """ Perform a POST request to host """
        self.request = HttpRequestMessage('POST', page, 
                                              self.host, headers, data)
        self.do_request()

    def head(self, page='/', headers=None):

        """ Perform a HEAD request to host """
        self.request = HttpRequestMessage('HEAD', page, self.host, headers)
        self.do_request()

    def do_request(self):

        """ Send request message to destination server """
        s = WebSocket(self.host, self.port)
        s.send(self.request.message)
        response, headers, body = self.receive_response(s)
        self.response = HttpResponseMessage(response, headers, body)
        if self.redirect_count > 3: #Caught in possible redirect loop
            print "Error: Redirect loop detected. Exiting."
            sys.exit(1)
        if self.response.get_status_code() in (301, 302):
            self.redirect_count += 1
            page = self.parse_location(headers.get('Location', ''))
            self.get(page)

    def check_port(self):

        """ Checks to see if port is attached to host """
        parsed_host = self.host.strip('http').strip('https').strip('//')
        if ':' in parsed_host:
            self.host, port = parsed_host.split(':')
            s = port.find('/')
            q = port.find('?')
            if s != -1:
                port = port[:s]
            elif q != -1:
                port = port[:q]
            elif len(port) > 0:
                return int(port)
        return 80

    def parse_location(self, loc):

        """ Splits location header value into host and page """
        loc = loc.replace('http:', '').replace('https:', '').replace('//', '')
        s = loc.find('/')
        self.host = loc[:s]
        return loc[s:]

    def receive_response(self, sock):

        """ Parse server HTTP response """
        response = sock.readline()
        headers = self.parse_headers(sock.recv(until='\r\n'))

        size, body = -1, ""
        if 'Content-Length' in headers:
            size = int(headers['Content-Length'])
            body = sock.recv(size=size)
        elif headers.get('Transfer-Encoding') == "chunked":
            while size != 0:
                size = int(sock.readline(), 16)
                body += sock.recv(size=size)
                sock.readline() # pass over \r\n
        else:
            print "ERROR: No length specified in headers"

        return (response, headers, body)

    def parse_headers(self, header_data):

        """ Converts header string into dictionary """
        headers = [k.split(':') for k in header_data.split('\r\n') if k]
        return {k[0].strip():':'.join(k[1:]).strip() for k in headers}
