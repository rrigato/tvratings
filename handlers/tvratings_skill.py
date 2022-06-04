from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type

import logging


logging.getLogger().setLevel(logging.INFO)


def alexa_lambda_handler(lambda_event, context):
    """Stub lambda handler test"""
    logging.info(dir(AbstractRequestHandler))


if __name__ == "__main__":
    import json
    import os
    os.environ["AWS_REGION"] = "us-east-1"
