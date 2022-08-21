class ResponseSuccess():
    """Value Object where usecase executed sucessfully, returning output of business logic
    """
    def __bool__(self):
        return(True)

    def __init__(self, response_value):
        self._response_value = response_value

    @property
    def response_value(self):
        return(self._response_value)




class ResponseFailure():
    """Value Object where error occurred when processing the usecase
    """
    def __bool__(self):
        return(False)

    def __init__(self, error_message):
        if type(error_message) != str:
            raise TypeError("ResponseFailure - error_message datatype must be a str")
        self._error_message = error_message

    @property
    def error_message(self):
        return(self._error_message)

