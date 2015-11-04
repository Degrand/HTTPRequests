import pytest

from HTTPRequests.message import HttpRequestMessage,  HttpResponseMessage

class Message_Testing(object):

    def test_HttpRequestMessage_init():

        msg_no_body =  HttpRequestMessage("GET", "/", {})
        msg_w_body =  HttpRequestMessage("POST", "/", {}, "body stuff")
        msg_w_headers = HttpRequestMessage("GET", "/test", 
                                           {'Accept': 'application/ld+json'})

        assert msg_no_body.method == "GET"
        assert msg_no_body.page == "/"
        assert msg_no_body.headers == {}
        assert msg_no_body.body == ""

        assert msg_w_body.method == "POST"
        assert msg_w_body.page == "/"
        assert msg_w_body.headers == {}
        assert msg_w_body.body == "body stuff"

        assert msg_w_headers.method == "GET"
        assert msg_w_headers.page == "/"
        assert msg_w_headers.headers == {}
        assert msg_w_headers.body == ""
