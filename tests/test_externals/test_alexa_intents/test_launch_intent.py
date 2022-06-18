from copy import deepcopy

import json
import unittest

class TestLaunchIntent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/events/intent_requests/launch_intent.json", "r") as intent_request:
            cls.intent_request = json.load(intent_request)

    def test_launch_intent(self):
        """LaunchRequest for initally opening the skill"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

        expected_message = "Welcome to the toonami television ratings provider"


        alexa_lambda_handler = get_alexa_lambda_handler()



        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )


        self.assertTrue(
            expected_message in actual_response_message["response"]["outputSpeech"]["ssml"],
            msg=f"""
                Expected Alexa Response - 
                {expected_message} 
                Actual Alexa Response - 
                {actual_response_message["response"]["outputSpeech"]["ssml"]}
            """
        )


