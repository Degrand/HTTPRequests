import pytest

from HTTPRequests.message import HttpRequestMessage,  HttpResponseMessage

def test_message_init_no_body():

    """ Test message construction without a body.
        e.g. standard GET request
    """
    msg_no_body =  HttpRequestMessage("GET", "/", 'localhost', {})

    assert msg_no_body.method == "GET"
    assert msg_no_body.page == "/"
    assert msg_no_body.headers == msg_no_body.create_headers()
    assert msg_no_body.body == ""

def test_message_init_w_body():

    """ Test message construction with body content.
        e.g. standard POST request
    """
    msg_w_body =  HttpRequestMessage("POST", "/", '192.168.0.1', {},
                                         body="body stuff")
    assert msg_w_body.method == "POST"
    assert msg_w_body.page == "/"
    assert msg_w_body.headers == msg_w_body.create_headers()
    assert msg_w_body.body == "body stuff"

def test_message_init_w_headers():

    """ Test message with modified headers.
        Verify supplied headers overwrite defaults.
    """
    msg_w_headers = HttpRequestMessage("GET", "/test", '127.0.0.1',
                                           headers={'Accept':
                                                    'application/ld+json'})

    assert msg_w_headers.method == "GET"
    assert msg_w_headers.page == "/test"
    assert msg_w_headers.headers == msg_w_headers.create_headers({'Accept':
                                                    'application/ld+json'})
    assert msg_w_headers.body == ""

def test_create_request_no_cust_ver():

    """ Test message for default version (1.1) and correct syntax

    """
    msg_no_cust_ver = HttpRequestMessage("GET", "/mypage", 'localhost', {})

    msg_str = "GET /mypage HTTP/1.1\r\n"

    assert msg_no_cust_ver.create_request() == msg_str

def test_create_request_cust_ver():

    """ Test message for custom HTTP version

    """
    msg_cust_ver = HttpRequestMessage("GET", "/yourpage", 'localhost', {}, 
                                          http_version='0.9')

    msg_str = "GET /yourpage HTTP/0.9\r\n"

    assert msg_cust_ver.create_request() == msg_str

def test_create_GET_headers():

    """ Test default created GET headers for expected structure

    """
    msg_get = HttpRequestMessage("GET", "/", 'localhost', {})
    get_headers = msg_get.create_GET_headers()
    assert 'accept' == get_headers[0][0]
    assert get_headers[0][1] != None
    assert 'date' == get_headers[1][0]
    assert get_headers[1][1] != None

def test_create_POST_headers():

    """ Test default created POST headers for expected structure

    """
    msg_post = HttpRequestMessage("POST", "/", 'localhost', {})
    post_headers = msg_post.create_POST_headers()
    assert 'content-type' == post_headers[0][0]
    assert post_headers[0][1] != None
    assert 'content-length' == post_headers[1][0]
    assert post_headers[1][1] >= 0
    assert 'accept' == post_headers[2][0]
    assert post_headers[2][1] != None

def test_merge_header_vals():

    """ Test header merge function for correct datastructure
        and value preferences
    """
    msg = HttpRequestMessage("GET", "/", 'localhost', {})
    header_vals = [('connection', 'keep-alive'),
                   ('host', 'localhost'),
                   ('from', 'bot@no.com'),
                   ('user-agent', 'RequestBot_0.1'),
                   ('cookie', ''),
                   ('accept', '*/*')]

    headers = {'Accept': 'application/ld+json'}
    h_dict = msg.merge_header_vals(header_vals, headers)

    assert 'Connection' in h_dict
    assert 'Host' in h_dict
    assert 'Cookie' not in h_dict
    assert 'Accept' in h_dict
    assert h_dict['Accept'] == 'application/ld+json'

def test_create_header_str():

    """ Test header string for correct syntax and expected order

    """
    headers = {'Accept': 'application/json',
               'Connection': 'keep-alive',
               'User-Agent': 'RequestBot_0.1',
               'From': 'bot@no.com',
               'Host': 'localhost',
               'Date': '2015-01-01'}

    expec_str = ("From: bot@no.com\r\n"
                 "Connection: keep-alive\r\n"
                 "Accept: application/json\r\n"
                 "User-Agent: RequestBot_0.1\r\n"
                 "Host: localhost\r\n"
                 "Date: 2015-01-01\r\n")

    msg_w_headers = HttpRequestMessage("GET", "/", 'localhost', headers)
    header_str = msg_w_headers.create_header_str()
    assert header_str == expec_str
