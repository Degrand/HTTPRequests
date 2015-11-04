import pytest

from HTTPRequests.message import HttpRequestMessage,  HttpResponseMessage

def test_message_init_no_body():

    msg_no_body =  HttpRequestMessage("GET", "/", 'localhost', {})

    assert msg_no_body.method == "GET"
    assert msg_no_body.page == "/"
    assert msg_no_body.headers == msg_no_body.create_headers()
    assert msg_no_body.body == ""

def test_message_init_w_body():

    msg_w_body =  HttpRequestMessage("POST", "/", '192.168.0.1', {},
                                         body="body stuff")
    assert msg_w_body.method == "POST"
    assert msg_w_body.page == "/"
    assert msg_w_body.headers == msg_w_body.create_headers()
    assert msg_w_body.body == "body stuff"

def test_message_init_w_headers():

    msg_w_headers = HttpRequestMessage("GET", "/test", '127.0.0.1',
                                           headers={'Accept':
                                                    'application/ld+json'})

    assert msg_w_headers.method == "GET"
    assert msg_w_headers.page == "/test"
    assert msg_w_headers.headers == msg_w_headers.create_headers({'Accept':
                                                    'application/ld+json'})
    assert msg_w_headers.body == ""
