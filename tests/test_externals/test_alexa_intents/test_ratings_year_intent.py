from copy import deepcopy
from unittest.mock import MagicMock
from unittest.mock import patch

import unittest

class TestRatingsYearIntent(unittest.TestCase):


    @patch("externals.alexa_intents.ratings_year_intent.year_ratings_summary")
    @patch("externals.alexa_intents.ratings_year_intent.get_valid_date")
    def test_ratings_year_intent(self, 
        get_valid_date_mock: MagicMock, 
        year_ratings_summary_mock: MagicMock):
        """RatingsYearIntentHandler.handle executes succesfully"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from fixtures.ratings_fixtures import mock_ratings_year_intent
        from tvratings.entry.response_objects import ResponseSuccess
        from tvratings.entry.request_objects import ValidRequest
        
        expected_message = "stub ratings year response"


        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            mock_ratings_year_intent(),
            None
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

