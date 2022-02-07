from datetime import date

class ShowAggregate:
    """Custom aggregration for a show"""

    def __init__(self):
        """Initialize all attributes to None"""
        pass


class TelevisionRating:
    """Custom aggregration for a show"""

    def __init__(self):
        """Initialize all attributes to None"""
        self.show_air_date = None
        self.timeslot = None
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