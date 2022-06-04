from copy import deepcopy
from unittest.mock import patch

import json
import unittest

class TestSessionEndedRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/events/intent_requests/session_ended_request.json", "r") as intent_request:
            cls.intent_request = json.load(intent_request)

    @patch("externals.alexa_intents.intent_dispatcher.SessionEndedRequestHandler.handle")
    def test_session_ended_request(self, mock_handle):
        """If cleanup logic is ever required, write test case here"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler


        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )

        self.assertEqual(mock_handle.call_count, 1)