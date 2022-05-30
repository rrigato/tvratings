
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def alexa_lambda_handler():
    """Stub lambda handler"""
    pass


if __name__ == "__main__":
    import json
    import os
    os.environ["AWS_REGION"] = "us-east-1"
