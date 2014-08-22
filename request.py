"""
    This module handles HTTP requests. It currently only supports basic
    GET and POST behavior

"""

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
        self.send_request()

    def post(self, page, headers=None, data=""):

        """ Perform a POST request to server """

        self.request = Message('POST', page, self.dest)
        self.send_request()

    def send_request(self):

        """ Send request message to destination server """
        s = WebSocket(self.dest, 80)
        s.send(self.request.message)
        response, headers, body = self.recieve_response(s)
        self.response = HttpResponseMessage(response, headers, body)

    def recieve_response(self, sock):

        """ Parse server HTTP response """
        response = sock.readline()
        headers = self.parse_headers(sock.recv(until='\r\n'))
        bodysize = self.get_bodysize(headers, sock)
        body = sock.recv(size=bodysize)
        return (response, headers, body)

    def get_bodysize(self, headers, sock):

        """ Find appropriate header for packet size """
        if 'Content-Length' in headers:
            size = int(headers['Content-Length'])
        elif headers.get('Transfer-Encoding') == 'chunked':
            size = int(sock.readline(), 16)
        else:
            print "ERROR: No length specified in headers"
            size = 0
        return size

    def parse_headers(self, header_data):

        """ Converts header string into dictionary """
        headers = [k.split(':') for k in header_data.split('\r\n') if k]
        return {clean(k[0]):clean(k[1]) for k in headers}
        
def clean(val):

    """ Remove whitespace and return characters from value """
    return val.rstrip().lstrip()
