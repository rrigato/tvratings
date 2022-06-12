from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.response import Response

import logging

class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent handler"""

    def can_handle(self, handler_input: HandlerInput):
        """Determines the type of input the class can handle

            Returns
            -------
            can_class_handle_request: bool
                True if this class can handle the provided request, False otherwise
        """
        return(is_intent_name("AMAZON.FallbackIntent")(handler_input))


    def handle(self, handler_input: HandlerInput) -> Response:
        """Applies business logic for the appropriate class handler"""

        logging.info("In FallbackIntentHandler")
        speech = "Hmm, I am not sure. Try asking me for the television ratings."

        return(handler_input.response_builder.speak(speech).ask(speech).response)

        