HTTPRequests
------------------

This is an attempt at building yet another http library for educational purposes. Any critiques or comments are welcome. I'm using [RFC2616](http://www.w3.org/Protocols/rfc2616/rfc2616.html) and [RFC7230](http://tools.ietf.org/html/rfc7230) as the primary guides for this code, and testing it against popular web services (google, amazon, facebook, etc.)

Example Usage:
-----------------

    from HTTPRequests.request import HttpRequest

    req = HttpRequest('www.w3c.org')
    resp = req.get('/Protocols/rfc2616/ref2616.html')
    print resp #This will print response body
