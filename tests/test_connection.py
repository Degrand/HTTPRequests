"""
    This module handles testing for WebSocket objects

    *** NOTE: This module currently requires an active internet connection ***

"""

import pytest

from HTTPRequests.connection import WebSocket

def test_websocket_init_noport():

    ws = WebSocket("www.google.com")
    assert ws.port == 80

def test_websocket_init_badport():

   with pytest.raises(OverflowError):
       ws = WebSocket("www.google.com", -23)

def test_websocket_init_diffport():

   ws = WebSocket("www.google.com", 443)
   assert ws.port == 443
