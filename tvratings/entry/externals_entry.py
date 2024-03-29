from copy import deepcopy
from datetime import datetime
from tvratings.entities.entity_model import TelevisionRating
from tvratings.entities.entity_model import YearRatingSummary
from tvratings.entry.input_valdiators import validate_iso_8601_date 
from tvratings.entry.request_objects import ValidRequest 
from tvratings.entry.request_objects import InvalidRequest 
from tvratings.entry.response_objects import ResponseFailure 
from tvratings.entry.response_objects import ResponseSuccess 
from tvratings.repo.tvratings_backend import load_one_date 
from tvratings.repo.tvratings_backend import load_one_year
from tvratings.usecase.ratings_business_rules import filter_by_rating
from tvratings.usecase.ratings_business_rules import select_highest_ratings
from tvratings.usecase.ratings_business_rules import select_lowest_ratings
from typing import Union

import logging

def get_valid_date(tvratings_day: str) -> Union[ValidRequest, InvalidRequest]:
    """Request object for invoking an interface that requires a datetime.date input

        Parameters
        ----------
        tvratings_day: str
            ISO 8601 YYYY-MM-DD format

        Returns
        -------
        valid_date_request: ValidRequest or InvalidRequest
            ValidRequest with request_filters
            {
                ratings_date: datetime.date
            }
            or InvalidRequest
    """
    logging.info("get_valid_date - beginning input validation")
    valid_date, date_parse_error = validate_iso_8601_date(iso_formatted_str=tvratings_day)
    
    if date_parse_error is not None:
        logging.info("get_valid_date - InvalidRequest returned")
        return(InvalidRequest(error_message=date_parse_error))

    logging.info("get_valid_date - ValidRequest returned")
    
    return(ValidRequest(request_filters={"ratings_date": valid_date}))

def get_one_night_ratings(valid_date_request: ValidRequest
    ) -> Union[ResponseSuccess, ResponseFailure]:
    """Gets TelevisionRating entities for one night

        Parameters
        ----------
        valid_date_request: tvratings.entry.externals_entry.get_valid_date output

        Returns
        -------
        tvratings_response: ResponseSuccess or ResponseFailure
            ResponseSuccess.response_value tvratings.repo.tvratings_backend.load_one_date

            [] if no TelevisionRating entites match ratings_date provided in the request_filter 
    """
    logging.info("get_one_night_ratings - new television request")
    television_ratings, load_one_date_error = load_one_date(
        ratings_occurred_on=valid_date_request.request_filters["ratings_date"]
    )
    
    if load_one_date_error is not None:
        logging.info("get_one_night_ratings - load_one_date_error")
        return(ResponseFailure(error_message=load_one_date_error))

    logging.info("get_one_night_ratings - returning ResponseSuccess")
    
    return(ResponseSuccess(response_value=deepcopy(television_ratings)))
    


def valid_year(year_to_validate: int) -> tuple[
        Union[int, None], Union[str, None]]:
    """returns int, None if year_to_validate is valid
    otherwise returns None, error_message
    """
    if year_to_validate < 2012:
        return(None, "Provided year must be greater than 2012")

    if datetime.today().year < year_to_validate:
        return(
            None, 
            f"Year must be less than or equal to {year_to_validate}")
    
    return(year_to_validate, None)




def _orchestrate_ratings_summary(
    year_of_ratings: list[TelevisionRating]) -> Union[
    YearRatingSummary, ResponseFailure]:
    """assumes year_of_ratings is not None
    """
    ratings_summary_instance = YearRatingSummary()
    year_of_ratings = filter_by_rating(year_of_ratings)

    if len(year_of_ratings) == 0:
        logging.info(
            "_orchestrate_ratings_summary - all ratings" +
            "dropped in data quality filter"
        )
        ResponseFailure(
            error_message="No ratings passed data quality check"
        )

    
    ratings_summary_instance.highest_rating = select_highest_ratings(
        year_of_ratings
    )

    logging.info(
        "_orchestrate_ratings_summary - obtained highest rating")

    ratings_summary_instance.lowest_rating = select_lowest_ratings(
        year_of_ratings
    )

    logging.info(
        "_orchestrate_ratings_summary - obtained lowest rating")

    return(ratings_summary_instance)



def year_ratings_summary(rating_year: int) -> Union[
    YearRatingSummary, ResponseFailure]:
    """Summary statistics for the provided rating_year
    """
    year_of_ratings, ratings_retrieval_error = load_one_year(
        rating_year)

    if ratings_retrieval_error is not None:
        logging.info(
            "year_ratings_summary - propagating unexpected error"
        )
        return(ResponseFailure(
            error_message=ratings_retrieval_error
        ))

    logging.info(
        f"year_ratings_summary - ratings retrieved for - {rating_year}"
    )
    
    if len(year_of_ratings) == 0:
        logging.info(
            "year_ratings_summary - no tv ratings for year"
        )
        return ResponseFailure(
            error_message="No ratings found for provided year"
        )
    
    logging.info("year_ratings_summary - invoking private interfaces")

    return(_orchestrate_ratings_summary(year_of_ratings))



if __name__ == "__main__":
    from time import strftime
    import logging
    import os
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" 
        + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.info
    )
    entry_response = year_ratings_summary(2014)

    if bool(entry_response):
        print(entry_response.lowest_rating.show_name)
        print(entry_response.lowest_rating.rating)
        print(entry_response.highest_rating.show_name)
        print(entry_response.highest_rating.rating)
    
    if bool(entry_response) == False:
        print(entry_response.error_message)
