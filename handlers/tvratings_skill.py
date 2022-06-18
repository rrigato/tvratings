from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

import logging


logging.getLogger().setLevel(logging.INFO)


alexa_lambda_handler = get_alexa_lambda_handler()


if __name__ == "__main__":
    import json
    import os
    os.environ["AWS_REGION"] = "us-east-1"
