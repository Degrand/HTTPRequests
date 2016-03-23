""" This module tests the functionality of the Cookie object """

from HTTPRequests.cookie import Cookie

def test_cookie_init_no_attrs():

    """ Tests to make sure basic variable assignment works for Cookie """
    oatmeal = Cookie("SpecCookie", 1234, "mydomain.com", "/login")
    assert oatmeal.name == "SpecCookie"
    assert oatmeal.value == 1234
    assert oatmeal.domain == "mydomain.com"
    assert oatmeal.path == "/login"
    assert any([x for x in oatmeal.attributes.values()]) == False

def test_cookie_init_w_attrs():

    """ Tests to make sure attributes are assigned correctly """
    attrs = {"Expires": "2030-01-01T00:00:00",
             "Max-Age": 9024,
             "Secure": True,
             "HttpOnly": True}
    pbutter = Cookie("Spoon", "Yes", "pbj.com", "/", expires=attrs["Expires"], 
                     maxage=attrs["Max-Age"])

    assert pbutter.attributes["Expires"] == "2030-01-01T00:00:00"
    assert pbutter.attributes["Max-Age"] > 9000
    assert pbutter.attributes["HttpOnly"] == False
    assert pbutter.attributes["Raw-String"] == None  

def test_set_cookie_str():

    """ Tests to make sure the cookie str is constructed as expected """
    chocolate = Cookie("Chips", 0, "cho.co", "/late")
    assert chocolate.cookie_str == "Chips=0;"
