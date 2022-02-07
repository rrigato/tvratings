from datetime import date



class TelevisionRating:
    """Television rating for one night, one timeslot, one show"""

    def __init__(self):
        """Initialize all attributes to None"""
        self.show_air_date = None
        self.time_slot = None
        self.show_name = None
        self.rating = None
        self.rating_18_49 = None
        self.household = None
        self.household_18_49 = None

    @property
    def show_air_date(self):
        return(self._show_air_date)

    @show_air_date.setter
    def show_air_date(self, show_air_date):
        if type(show_air_date) not in (date, type(None)):
            raise TypeError("TelevisionRating - show_air_date datatype must be a date")
        self._show_air_date = show_air_date


    @property
    def time_slot(self):
        return(self._time_slot)

    @time_slot.setter
    def time_slot(self, time_slot):
        if type(time_slot) not in (str, type(None)):
            raise TypeError("TelevisionRating - time_slot datatype must be a str")
        self._time_slot = time_slot


    @property
    def show_name(self):
        return(self._show_name)

    @show_name.setter
    def show_name(self, show_name):
        if type(show_name) not in (str, type(None)):
            raise TypeError("TelevisionRating - show_name datatype must be a str")
        self._show_name = show_name


    @property
    def rating(self):
        return(self._rating)

    @rating.setter
    def rating(self, rating):
        if type(rating) not in (int, type(None)):
            raise TypeError("TelevisionRating - rating datatype must be a int")
        self._rating = rating


    @property
    def rating_18_49(self):
        return(self._rating_18_49)

    @rating_18_49.setter
    def rating_18_49(self, rating_18_49):
        if type(rating_18_49) not in (int, type(None)):
            raise TypeError("TelevisionRating - rating_18_49 datatype must be a int")
        self._rating_18_49 = rating_18_49


    @property
    def household(self):
        return(self._household)

    @household.setter
    def household(self, household):
        if type(household) not in (float, type(None)):
            raise TypeError("TelevisionRating - household datatype must be a float")
        self._household = household


    @property
    def household_18_49(self):
        return(self._household_18_49)

    @household_18_49.setter
    def household_18_49(self, household_18_49):
        if type(household_18_49) not in (float, type(None)):
            raise TypeError("TelevisionRating - household_18_49 datatype must be a float")
        self._household_18_49 = household_18_49




class RatingMetric:
    """Television rating for one night, one timeslot, one show"""

    def __init__(self):
        """Initialize all attributes to None"""
        self.metric_key = None
        self.metric_description = None
        self.rating = None
        self.rating_18_49 = None
        self.household = None
        self.household_18_49 = None
        '''
            TODO - test cases and implementation
            parameterize existing test cases?
        '''



