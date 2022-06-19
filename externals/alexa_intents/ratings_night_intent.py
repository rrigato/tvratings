from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_slot
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response
from tvratings.entry.externals_entry import get_valid_date

import logging



def _get_intent_slot_value(handler_input: HandlerInput, slot_name: str) -> str:
    """loads the slot_name from handler_input or returns None"""
    try:
        return(get_slot(handler_input=handler_input, slot_name="burn_location").value)
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

    
    logging.info(f"""
        _orchestrate_ratings_retrieval - ratings_date -
            {valid_ratings_night.request_filters["ratings_date"]}
        """)
        
    return(valid_ratings_night.request_filters["ratings_date"])




class RatingsNightIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
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
                .ask(entry_response_message)
                .response
        )
