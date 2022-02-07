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
        
