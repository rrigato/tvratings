from ask_sdk_core.skill_builder import SkillBuilder
from externals.alexa_exceptions.default_graceful_exit import DefaultExceptionHandler
from externals.alexa_requests.session_ended_request import SessionEndedRequestHandler

import logging


def get_alexa_lambda_handler():
    """Retrieves a lambda_handler function after binding all custom skill intent request and
    exception objects

        Returns
        -------
        alexa_lambda_handler: function
            wrapper around a traditional lambda function that takes a lambda_event and lambda_context
            object for an alexa skill
            https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/api/core.html?highlight=lambda_handler#ask_sdk_core.skill_builder.SkillBuilder.lambda_handler


    """
    logging.info("get_alexa_lambda_handler - SkillBuilder")

    alexa_skill = SkillBuilder()

    '''
        request handlers are processed from top to bottom
    '''
    alexa_skill.add_request_handler(SessionEndedRequestHandler())

    alexa_skill.add_exception_handler(DefaultExceptionHandler())

    logging.info("get_alexa_lambda_handler - returning alexa_lambda_handler")

    return(alexa_skill.lambda_handler())