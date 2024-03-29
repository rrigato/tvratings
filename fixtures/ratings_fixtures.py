from copy import deepcopy
from datetime import date
from random import randint
from random import paretovariate
from tvratings.entities.entity_model import TelevisionRating
from tvratings.entities.entity_model import YearRatingSummary
from typing import Union

import json


def get_mock_television_ratings(number_of_ratings: int) -> list[TelevisionRating]:
    """Creates a list of mock TelevisionRating entities

        Parameters
        ----------
        number_of_ratings: int
            number of mock TelevisionRating elements to create
            Assumes, but does not validate, being less than 12

        Returns
        -------
        television_ratings_list: list
            each element is a TelevisionRating entity
    """
    television_ratings_list = []

    for rating_num in range(number_of_ratings):

        mock_television_rating = TelevisionRating()

        mock_television_rating.show_air_date = date.fromisoformat("2014-01-04")
        mock_television_rating.time_slot = str(rating_num) + ":00 am"
        mock_television_rating.show_name = "MOCK_SHOW" + str(rating_num)
        mock_television_rating.rating = min(int(100 * paretovariate(1)), 9999)
        mock_television_rating.rating_18_49 = max(
            int(mock_television_rating.rating - (10*paretovariate(3))), 25
        )
        mock_television_rating.household = round(paretovariate(2) / 10, 2)
        mock_television_rating.household_18_49 = max(
            round(mock_television_rating.household - (10*paretovariate(3))), .05
        )
        mock_television_rating.rating_year = randint(2012, 3005)

        television_ratings_list.append(mock_television_rating)

    return(deepcopy(television_ratings_list))




def fake_dynamodb_query_response(number_of_ratings: int) -> dict[str, Union[int, list]]:
    """AWS SDK Dynamodb query response

        Parameters
        ----------
        number_of_ratings: 
            How many mock ratings elements you want in the Items key

        Returns
        -------
        Response structure for sdk documented here:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.query
        
    """
    sdk_response = {
        "Items": [],
        "Count": number_of_ratings,
        "ScannedCount": number_of_ratings
    }
    for tv_show in get_mock_television_ratings(number_of_ratings):
        sdk_response["Items"].append({
            "RATINGS_OCCURRED_ON": tv_show.show_air_date.isoformat(),
            "TIME": tv_show.time_slot,
            "SHOW": tv_show.show_name,
            "PERCENTAGE_OF_HOUSEHOLDS_AGE_18_49": str(tv_show.household_18_49),
            "PERCENTAGE_OF_HOUSEHOLDS": str(tv_show.household),
            "TOTAL_VIEWERS_AGE_18_49": str(tv_show.rating_18_49),
            "TOTAL_VIEWERS": str(tv_show.rating),
            "YEAR": str(tv_show.rating_year)
        })

    return(deepcopy(sdk_response))


def mock_year_rating_summary() -> YearRatingSummary:
    """mock YearRatingSummary with all fields populated

    Raises
    ------
    AssertionError
        Raised if YearRatingSummary().highest_rating
        is less than or equal YearRatingSummary().lowest_rating
    """
    mock_tv_ratings = get_mock_television_ratings(2)
    
    '''Double the properties of mock TelevisionRating
    element 0 to create a simulated low and high tv rating
    '''
    mock_tv_ratings[0].household = mock_tv_ratings[1].household * 2
    mock_tv_ratings[0].household_18_49 = (
        mock_tv_ratings[1].household_18_49 * 2
    )
    mock_tv_ratings[0].rating = mock_tv_ratings[1].rating * 2
    mock_tv_ratings[0].rating_18_49 = (
        mock_tv_ratings[1].rating_18_49 * 2
    )
    
    mock_year_rating_summary = YearRatingSummary()

    mock_year_rating_summary.highest_rating = mock_tv_ratings[0]

    mock_year_rating_summary.lowest_rating = mock_tv_ratings[1]

    assert (
        mock_year_rating_summary.highest_rating.rating >
        mock_year_rating_summary.lowest_rating.rating 
    ), f"""
    highest_rating {mock_year_rating_summary.highest_rating.rating} 
    property not higher than 
    lowest_rating {mock_year_rating_summary.lowest_rating.rating} """
        
    return(mock_year_rating_summary)


def mock_year_high_low_intent() -> dict:
    """deepcopied returned from this file location
    tests/events/intent_requests/year_high_low_intent.json
    """
    with open("tests/events/intent_requests/year_high_low_intent.json",
        "r") as intent_json:
        intent_request = json.load(intent_json)

    return(deepcopy(intent_request))


def mock_ratings_year_intent() -> dict:
    """Loads the RatingsYearIntent json as a dict from here
    tests/events/intent_requests/ratings_year_intent.json
    """
    with open(
        "tests/events/intent_requests/ratings_year_intent.json", 
        "r") as intent_request:
        intent_request = json.load(intent_request)

    return(deepcopy(intent_request))

