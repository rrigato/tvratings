from fixtures.ratings_fixtures import get_mock_television_ratings
from typing import Union
from tvratings.entities.entity_model import TelevisionRating


def load_one_date(ratings_occurred_on) -> tuple[Union[list[TelevisionRating], None], Union[str, None]] :
    """Loads all television ratings for one saturday night

        Parameters
        ----------
        ratings_occurred_on: datetime.date
            Saturday night ratings date

        Returns
        -------
        television_ratings: list
            Each element is a TelevisionRating entity
            No matching ratings for ratings_occurred_on returns []
            Any unexpected processing errors returns None

        unexpected_error: None
            str if unable to load the television ratings from persistent storage 
    """
    '''TODO - Implement'''
    return(get_mock_television_ratings(2), None)