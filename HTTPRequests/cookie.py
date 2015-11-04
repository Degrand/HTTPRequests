class Cookie(object):

    """ Encapsulates the values of an HTTP Cookie """
    def __init__(self, name, value, domain, path, **kwargs):
        self.name = name
        self.value = value
        self.path = path
        self.domain = domain
        self.expires = kwargs.get('Expires')
        self.max_age = kwargs.get('Max-Age')
        self.secure = kwargs.get('Secure', False)
        self.httponly = kwargs.get('HttpOnly', False)
        self.raw_str = kwargs.get('Raw-String')
        self.cookie_str = self.set_cookie_str()

    def __str__(self):

        return self.cookie_str

    def set_cookie_str(self):

        """ Creates HTTP valid cookie string """
        return "%s=%s;" % (self.name, self.value)
