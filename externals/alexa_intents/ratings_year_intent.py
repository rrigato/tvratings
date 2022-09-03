from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_slot
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response
from tvratings.entities.entity_model import TelevisionRating
from tvratings.entry.externals_entry import get_valid_date
from tvratings.entry.externals_entry import get_one_night_ratings

import logging



class RatingsYearIntentHandler(AbstractRequestHandler):
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

        logging.info("RatingsYearIntentHandler - handle")
        
        entry_response_message = "stub ratings year response"

        return (
            handler_input.response_builder
                .speak(entry_response_message)
                .set_should_end_session(True)
                .response
        )

