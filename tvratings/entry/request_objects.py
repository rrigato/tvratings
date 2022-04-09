class ValidRequest():
    """Value object that can be used to invoke a usecase
    """
    def __bool__(self):
        return(True)

    def __init__(self, request_filters):
        if type(request_filters) not in (dict, type(None)):
            raise TypeError("ValidRequest - request_filters datatype must be a dict")
        self._request_filters = request_filters

    @property
    def request_filters(self):
        return(self._request_filters)



class InvalidRequest():
    """Value object that returns an invalid request to client with error_message
    """
    def __bool__(self):
        return(False)

    def __init__(self, error_message):
        if type(error_message) not in (str, type(None)):
            raise TypeError("InvalidRequest - error_message datatype must be a str")
        self._error_message = error_message

    @property
    def error_message(self):
        return(self._error_message)
