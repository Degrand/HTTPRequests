import socket

class WebSocket(object):

    """ Simple socket class to handle TCP messaging between servers"""

    def __init__(self, host, port):

        """ Websocket composed of a host (ip) and port number """
        self.host = host
        self.port = port
        self.conn = self.connect()

    def connect(self):

        """ Establish connection with server """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

    def send(self, msg):

        """ Send HTTP request to host """
        self.conn.send(msg)

    def recv(self, size=1024):

        """ Recieve HTTP response from host """
        outdata, data = "", ""
        while not data.endswith('\r\n\r\n'): #This is a bad conditional
            data = self.conn.recv(size)
            outdata += data
        return outdata
