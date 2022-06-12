from copy import deepcopy

import json
import unittest

class TestFallbackIntent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/events/intent_requests/fallback_intent.json", "r") as intent_request:
            cls.intent_request = json.load(intent_request)

    def test_fallback_intent(self):
        """IntentRequest of type AMAZON.FallbackIntent contains expected response"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

        expected_message = "Hmm, I am not sure. Try asking me for the television ratings."


        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )

        self.assertTrue(
            expected_message in actual_response_message["response"]["outputSpeech"]["ssml"],
            msg="""\n
                Expected Alexa Response - 
                {expected_response} 
                \n
                Actual Alexa Response - 
                {actual_response}
            """.format(
                    expected_response=expected_message,
                    actual_response=actual_response_message["response"]["outputSpeech"]["ssml"]
                )
        )

        '''
            to ensure a reprompt message and the session is left open when the user 
            asks for help
        '''
        self.assertEqual(
            actual_response_message["response"]["outputSpeech"]["ssml"],
            actual_response_message["response"]["reprompt"]["outputSpeech"]["ssml"]
        )

        self.assertFalse(
            actual_response_message["response"]["shouldEndSession"]
        )
