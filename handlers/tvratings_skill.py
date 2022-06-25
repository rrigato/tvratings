from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

import logging


logging.getLogger().setLevel(logging.INFO)


alexa_lambda_handler = get_alexa_lambda_handler()




if __name__ == "__main__":
    from time import strftime
    import logging
    import json
    import os
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.DEBUG
    )
    with open("tests/events/intent_requests/ratings_night_intent.json", "r") as intent_request:
        intent_request = json.load(intent_request)

    alexa_lambda_handler(intent_request, None)