from copy import deepcopy
from unittest.mock import patch

import json
import unittest

class TestRatingsNightIntent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/events/intent_requests/ratings_night_intent.json", "r") as intent_request:
            cls.intent_request = json.load(intent_request)


    @unittest.skip("skipping for now")
    @patch("externals.alexa_intents.burn_status_intent.location_burn_status")
    @patch("externals.alexa_intents.burn_status_intent.validate_location_burn_status")
    def test_burn_status_intent(self, mock_validate_location_burn_status, 
        mock_location_burn_status):
        """BurnStatusIntentHandler.handle executes usecase and returns burn status"""
        from burnday.entities.entity_model import BurnStatus
        from burnday.entry.response_objects import ResponseSuccess
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler
        
        expected_message = "mock burn status message returned from usecase"
        mock_burn_status_entity = BurnStatus()
        mock_burn_status_entity.burn_status = expected_message
        mock_validate_location_burn_status.return_value = True
        mock_location_burn_status.return_value = ResponseSuccess(
            response_value=mock_burn_status_entity
        )

        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )


        mock_validate_location_burn_status.assert_called_once_with(
            zip_code=int(
                self.intent_request["request"]["intent"]["slots"]["burn_location"]["value"]
            )
        )

        self.assertTrue(
            expected_message in actual_response_message["response"]["outputSpeech"]["ssml"],
            msg=f"""\n
                Expected Alexa Response -
                {expected_message} 

                Actual Alexa Response - 
                {actual_response_message["response"]["outputSpeech"]["ssml"]}
            """
        )

        self.assertTrue(actual_response_message["response"]["shouldEndSession"])


    @patch("externals.alexa_intents.ratings_night_intent.RatingsNightIntentHandler.handle")
    def test_ratings_night_intent_unexpected_error(self, mock_burn_status_handle):
        """RatingsNightIntentHandler.handle raises unexpected errror that is handled gracefully"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

        alexa_lambda_handler = get_alexa_lambda_handler()

        mock_burn_status_handle.side_effect = TimeoutError("Unexpected Network timeout")

        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )

        self.assertEqual(type(actual_response_message["response"]["outputSpeech"]["ssml"]), str)
    
        self.assertTrue(actual_response_message["response"]["shouldEndSession"])

