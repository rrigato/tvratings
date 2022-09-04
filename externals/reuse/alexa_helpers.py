from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_slot

import logging

def get_intent_slot_value(handler_input: HandlerInput, 
    slot_name_to_select: str) -> str:
    """loads the slot_name_to_select from handler_input 
    or returns None"""
    try:
        return(
            get_slot(
                handler_input=handler_input, 
                slot_name=slot_name_to_select
            ).value
        )
    except Exception:
        logging.exception(
            "get_intent_slot_value - error retrieving slot")
        return(None)
