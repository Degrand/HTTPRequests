"""
    This module handles testing for WebSocket objects

    *** NOTE: This module currently requires an active internet connection ***

"""

import pytest

from HTTPRequests.connection import WebSocket

def test_websocket_init_noport():

    """ Tests to ensure a lack of port parameter defaults to 80 """
    ws = WebSocket("www.google.com")
    assert ws.port == 80

def test_websocket_init_badport():

   """ Tests negative and non-integer ports for proper error handling """
   with pytest.raises(OverflowError):
       ws = WebSocket("www.google.com", -23)
   with pytest.raises(TypeError):
       ws = WebSocket("www.google.com", 'a')
   with pytest.raises(TypeError):
       ws = WebSocket("www.google.com", None)

def test_websocket_init_diffport():

   """ Tests that the websocket will connect to non-80 ports when open """
   ws = WebSocket("www.google.com", 443)
   assert ws.port == 443
