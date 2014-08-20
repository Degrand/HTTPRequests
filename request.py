"""
    This module handles HTTP requests. It currently only supports basic
    GET and POST behavior

"""

import sys

from connection import WebSocket
from message import HttpRequestMessage, HttpResponseMessage

class HttpRequest(object):

    """ HTTP Request to server for some resource """

    def __init__(self, dest, debug=False):

        self.dest = dest 
        self.request = None
        self.response = None

    def get(self, page, headers=None):

        """ Perform a GET request to server """

        self.request = HttpRequestMessage('GET', page, self.dest)
        s = WebSocket(self.dest, 80)
        print self.request
        s.send(self.request.message)
        response, headers, body = self.split_response(s.recv())
        self.response = HttpResponseMessage(response, headers, body)

    def post(self, page, headers=None, data=""):

        """ Perform a POST request to server """

        self.request = Message('POST', page, self.dest)
        s = WebSocket(self.dest, 80)
        print self.request
        s.send(self.request.message)
        response, headers, body = self.split_response(s.recv())
        self.response = HttpResponseMessage(response, headers, body)

    def split_response(self, resp):

        """ Chops up raw_response into response, headers and body """
        s = resp.find('\r\n')
        response = resp[:s].rstrip()
        resp = resp[s+2:]
        s = resp.find('\r\n\r\n')
        header_data = resp[:s].rstrip()
        headers = self.parse_headers(header_data)
        if header_data.endswith('Transfer-Encoding: chunked'):
            body = resp[s+12:].rstrip().lstrip()
        else:
            body = resp[s+4:].rstrip().lstrip()

        return (response, headers, body)

    def parse_headers(self, header_data):

        """ Converts header string into dictionary """
        headers = [k.split(':') for k in header_data.split('\r\n')]
        return {k[0]:k[1] for k in headers}
        

if __name__ == "__main__":

    host = 'localhost'
    debug = False
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        debug = bool(sys.argv[2])
    hreq = HttpRequest(host, debug)
    hreq.get('/')
    print hreq.response
