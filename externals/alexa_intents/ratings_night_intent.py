from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_slot
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response
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



def _orchestrate_ratings_retrieval(handler_input: HandlerInput) -> str:
    """Orchestrates RequestObject and entry implementation to pull ratings
    """
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

    '''
        TODO - 
        load the list of TelevisionRatings from usecase
        parse high and low
        separate messages for ResponseFailure, ResponseSuccess([])
        or list of TelevisionRatings entities returned
    '''

    return(valid_ratings_night.request_filters["ratings_date"])




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
