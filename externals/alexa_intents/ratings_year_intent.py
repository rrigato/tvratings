from datetime import date
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_slot
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response
from externals.reuse.alexa_helpers import get_intent_slot_value
from tvratings.entities.entity_model import TelevisionRating
from tvratings.entry.externals_entry import valid_year
from tvratings.entry.externals_entry import year_ratings_summary

import logging



def _orchestrate_ratings_summary(handler_input: HandlerInput) -> str:
    """
    """
    try:
        logging.info(f"_orchestrate_ratings_summary - invocation begin")
        
        get_intent_slot_value(handler_input, "ratings_year_intent")
        parsed_year, year_retrieval_error = valid_year(
            int(
                get_intent_slot_value(
                    handler_input, "ratings_year"
                )
            )
        )

        if year_retrieval_error is not None:
            logging.info(
                f"_orchestrate_ratings_summary - {year_retrieval_error}")
            return("Invalid year provided - year must 4 digits" +
                f"from 2012 up until {date.today().year}"
            )

        year_ratings_summary(
            parsed_year
        )
        logging.info(f"_orchestrate_ratings_summary - invocation end")
        return("stub ratings year response")

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
        """Determines the type of input the class can handle

            Returns
            -------
            can_class_handle_request: bool
                True if this class can handle the provided request, False otherwise
        """
        return is_intent_name("RatingsYearIntent")(handler_input)


    def handle(self, handler_input: HandlerInput) -> Response:
        """Applies business logic for the appropriate class handler"""

        logging.info("RatingsYearIntentHandler - handle")
        
        

        return (
            handler_input.response_builder
                .speak(_orchestrate_ratings_summary(handler_input))
                .set_should_end_session(True)
                .response
        )

