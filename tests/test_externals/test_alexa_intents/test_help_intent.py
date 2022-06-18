from copy import deepcopy

import json
import unittest

class TestHelpIntent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/events/intent_requests/help_intent.json", "r") as intent_request:
            cls.intent_request = json.load(intent_request)

    def test_help_intent(self):
        """IntentRequest of type AMAZON.HelpIntent contains expected response"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

        expected_message = "Provide the date of the Saturday night you want television ratings for"


        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )

        self.assertTrue(
            expected_message in actual_response_message["response"]["outputSpeech"]["ssml"],
            msg=f"""\n
                Expected Alexa Response - 
                {expected_message}
                \n 
                Actual Alexa Response - 
                {actual_response_message["response"]["outputSpeech"]["ssml"]}
            """
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
