from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response

import logging

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """User requests AMAZON.CancelIntent or AMAZON.StopIntent during a session"""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        """Determines the type of input the class can handle

            Returns
            -------
            can_class_handle_request: bool
                True if this class can handle the provided request, False otherwise
        """
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))


    def handle(self, handler_input: HandlerInput) -> Response:
        """Applies business logic for the appropriate class handler"""
        
        speak_output = """
            <prosody rate="x-slow">
                <emphasis level="reduced">
                    <voice name="Joey">later</voice>
                </emphasis>
            </prosody>
        """

        logging.info("CancelOrStopIntentHandler.handle - cleanup complete")
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
