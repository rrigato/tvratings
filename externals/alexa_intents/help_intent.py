from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response

import logging

class HelpRequestHandler(AbstractRequestHandler):
    """Handler for when the user asks for help"""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        """Determines the type of input the class can handle
            Returns
            -------
            can_class_handle_request
                True if this class can handle the provided request, False otherwise
        """

        return(is_intent_name("AMAZON.HelpIntent")(handler_input))


    def handle(self, handler_input: HandlerInput) -> Response:
        """Applies business logic for the appropriate class handler"""
        output_message = "Provide the date of the Saturday night you want television ratings for"

        logging.info("HelpRequestHandler - handle")

        return(
            handler_input.response_builder
                .speak(output_message)
                .ask(output_message)
                .response
        )

