"""
    This module handles basic TCP connections for requests

"""

import socket

class WebSocket(object):

    """ Simple socket class to handle TCP messaging between servers """

    def __init__(self, host, port=80):

        """ Websocket composed of a host (ip) and port number """
        self.host = socket.gethostbyname(host)
        self.port = port
        self.conn = self.connect()
        self.rfile = self.conn.makefile()

    def connect(self):

        """ Establish connection with server """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def send(self, msg):

        """ Send HTTP request to host """
        self.conn.send(msg)

    def recv(self, size=1024, until=None):

        """ Recieve HTTP response from host """
        if until:
            line, outstring = "", ""
            while line != until:
                outstring += line
                line = self.rfile.readline()
            return outstring
        else:
            return self.rfile.read(size)

    def readline(self):

        """ Read a line off socket """
        return self.rfile.readline()
