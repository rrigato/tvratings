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


class YearRatingSummary():
    """Summary statistics from one year of television ratings"""
    def __bool__(self):
        return(True)

    def __init__(self):
        """Initialize all attributes to None"""
        self.highest_rating = None
        self.lowest_rating = None

    @property
    def highest_rating(self):
        return(self._highest_rating)

    @highest_rating.setter
    def highest_rating(self, highest_rating):
        if type(highest_rating) not in (int, type(None)):
            raise TypeError(
            "YearRatingSummary - highest_rating datatype must be a int"
            )
        self._highest_rating = highest_rating


    @property
    def lowest_rating(self):
        return(self._lowest_rating)

    @lowest_rating.setter
    def lowest_rating(self, lowest_rating):
        if type(lowest_rating) not in (int, type(None)):
            raise TypeError(
            "YearRatingSummary - lowest_rating datatype must be a int"
            )
        self._lowest_rating = lowest_rating

