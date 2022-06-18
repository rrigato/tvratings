from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.response import Response

import logging

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input: HandlerInput) -> bool:
        """Determines the type of input the class can handle

            Returns
            -------
            can_class_handle_request: bool
                True if this class can handle the provided request, False otherwise
        """
        return is_request_type("LaunchRequest")(handler_input)


    def handle(self, handler_input: HandlerInput) -> Response:
        """Applies business logic for the appropriate class handler"""

        skill_startup_message = "Welcome to the toonami television ratings provider"
        logging.info("LaunchRequestHandler - handle")
        
        return (
            handler_input.response_builder
                .speak(skill_startup_message)
                .ask(skill_startup_message)
                .response
        )
