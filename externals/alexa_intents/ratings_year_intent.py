from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response
from datetime import date
from externals.reuse.alexa_helpers import get_intent_slot_value
from tvratings.entry.externals_entry import valid_year
from tvratings.entry.externals_entry import year_ratings_summary

import logging



def _invoke_ratings_summary_entry(rating_year: int) -> str:
    """invocation and error checking for entry function
    """
    logging.info(f"_invoke_ratings_summary_entry - invocation begin")

    ratings_summary_response = year_ratings_summary(
        rating_year
    )

    if bool(ratings_summary_response) == False:
        logging.info(
            f"_invoke_ratings_summary_entry - ResponseFailure" +
            f"{ratings_summary_response.error_message}"
        )
        return(f"Unable to load ratings for {rating_year}")
    
    logging.info(f"_invoke_ratings_summary_entry - happy path")
    
    return(f"""
        The highest rated show for {rating_year} was 
        {ratings_summary_response.highest_rating.show_name} 
        on {ratings_summary_response.highest_rating.show_air_date} 
        with {ratings_summary_response.highest_rating.rating}  
        thousand viewers.

        The lowest rated show for {rating_year} was 
        {ratings_summary_response.lowest_rating.show_name} 
        on {ratings_summary_response.lowest_rating.show_air_date} 
        with {ratings_summary_response.lowest_rating.rating}  
        thousand viewers.
    """)



def _orchestrate_ratings_summary(handler_input: HandlerInput) -> str:
    """"""
    try:
        logging.info(f"_orchestrate_ratings_summary - invocation begin")
        
        parsed_year, year_retrieval_error = valid_year(
            int(
                get_intent_slot_value(
                    handler_input, "ratings_year"
                )
            )
        )

        if year_retrieval_error is not None:
            logging.info(
                f"_orchestrate_ratings_summary - {year_retrieval_error}"
            )
            return("Invalid year provided - year must be 4 digits" +
                f" from 2012 up until {date.today().year}"
            )

        logging.info(
            f"_orchestrate_ratings_summary - parsed_year {parsed_year}"
        )
        return(_invoke_ratings_summary_entry(parsed_year))

    except Exception as error_passthrough:
        logging.exception(
            "_orchestrate_ratings_summary - unexpected exception"
        )
        return(
            "Unexpected error occurred" +
            "when loading the television ratings"
        )


class RatingsYearIntentHandler(AbstractRequestHandler):
    """Handler for RatingsYearIntent"""
    def can_handle(self, handler_input: HandlerInput) -> bool:
        """True if this is a RatingsYearIntent, False otherwise
        """
        return(is_intent_name("RatingsYearIntent")(handler_input))


    def handle(self, handler_input: HandlerInput) -> Response:
        """Implements business logic for the intent"""

        logging.info("RatingsYearIntentHandler - handle")

        return (
            handler_input.response_builder
                .speak(_orchestrate_ratings_summary(handler_input))
                .set_should_end_session(True)
                .response
        )

