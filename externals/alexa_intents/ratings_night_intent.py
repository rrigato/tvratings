from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_slot
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response
from tvratings.entities.entity_model import TelevisionRating
from tvratings.entry.externals_entry import get_valid_date
from tvratings.entry.externals_entry import get_one_night_ratings

import logging



def _get_intent_slot_value(handler_input: HandlerInput, slot_name_to_select: str) -> str:
    """loads the slot_name_to_select from handler_input or returns None"""
    try:
        return(get_slot(handler_input=handler_input, slot_name=slot_name_to_select).value)
    except Exception:
        logging.exception("_get_intent_slot_value - error retrieving slot")
        return(None)




def _ratings_boundary_format(television_rating: TelevisionRating) -> str:
    """Applies calculation logic based on whether the rating is over or under 1 million
    """
    if television_rating.rating > 1000:
        logging.info("_ratings_boundary_format - over 1 million")
        return(f"{television_rating.rating/1000} million")
    
    logging.info("_ratings_boundary_format - under 1 million")

    return(f"{television_rating.rating} thousand")



def _format_response_message(television_ratings: list[TelevisionRating]) -> str:
    """Appropritate response str based on television_ratings list"""
    
    if len(television_ratings) == 0:
        logging.info("_format_response_message - no TelevisionRating entities returned")
        return("There are no television ratings for the night you selected")

    
    logging.info("_format_response_message - Iterating list")

    output_string = "The ratings for that Saturday night were: "

    for television_rating in television_ratings:
        output_string += f"""
            {television_rating.show_name} with 
            {_ratings_boundary_format(television_rating)} viewers.
        """

    logging.info(f"_format_response_message - {output_string}")

    return(output_string)


def _orchestrate_ratings_retrieval(handler_input: HandlerInput) -> str:
    """Orchestrates RequestObject and entry implementation to pull ratings
    """
    try:
        logging.info("_orchestrate_ratings_retrieval - invocation begin")
        
        valid_ratings_night = get_valid_date(
            _get_intent_slot_value(handler_input, "rating_occurred_on")
        )
        
        if bool(valid_ratings_night) is False:
            logging.info("_orchestrate_ratings_retrieval - InvalidRequestObject returned")
            return("Invalid television rating date provided")
        
        logging.info(f"""
            _orchestrate_ratings_retrieval - ratings_date -
                {valid_ratings_night.request_filters["ratings_date"]}
            """)


        one_night_ratings = get_one_night_ratings(valid_ratings_night)

        if bool(one_night_ratings) is False:
            logging.info(
                f"_orchestrate_ratings_retrieval - ResponseFailure {one_night_ratings.error_message}"
            )
            return("We encountered an error when loading the ratings for that night")
        
        logging.info("_orchestrate_ratings_retrieval - valid response")

        return(_format_response_message(one_night_ratings.response_value))

    except Exception as error_passthrough:
        logging.exception("_orchestrate_ratings_retrieval - unexpected exception suppression")
        return("Unexpected error occurred when loading the television ratings")




class RatingsNightIntentHandler(AbstractRequestHandler):
    """Handler for RatingsNightIntent"""
    def can_handle(self, handler_input: HandlerInput) -> bool:
        """Determines the type of input the class can handle

            Returns
            -------
            can_class_handle_request: bool
                True if this class can handle the provided request, False otherwise
        """
        return is_intent_name("RatingsNightIntent")(handler_input)


    def handle(self, handler_input: HandlerInput) -> Response:
        """Applies business logic for the appropriate class handler"""

        logging.info("RatingsNightIntentHandler - handle")
        
        entry_response_message = _orchestrate_ratings_retrieval(handler_input)

        return (
            handler_input.response_builder
                .speak(entry_response_message)
                .set_should_end_session(True)
                .response
        )

