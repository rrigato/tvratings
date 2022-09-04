from copy import deepcopy
from unittest.mock import MagicMock
from unittest.mock import patch

import unittest

class TestRatingsYearIntent(unittest.TestCase):


    @patch("externals.alexa_intents.ratings_year_intent.year_ratings_summary")
    def test_ratings_year_intent(self,  
        year_ratings_summary_mock: MagicMock):
        """RatingsYearIntentHandler.handle executes succesfully"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler
        from fixtures.ratings_fixtures import mock_ratings_year_intent
        from fixtures.ratings_fixtures import mock_year_rating_summary
        
        year_ratings_summary_mock.return_value = (
            mock_year_rating_summary()
        )

        
        expected_messages = [
            "The highest rated show for ",
            "The lowest rated show for "
        ]


        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            mock_ratings_year_intent(),
            None
        )


        args, kwars = year_ratings_summary_mock.call_args
        self.assertIsInstance(args[0], int)
        [
            self.assertTrue(
                expected_message in 
                actual_response_message["response"
                ]["outputSpeech"]["ssml"],
                msg=f"""\n
                    Expected Alexa Response -
                    {expected_message} 

                    Actual Alexa Response - 
                    {actual_response_message["response"
                    ]["outputSpeech"]["ssml"]}
                """
            )
            for expected_message in expected_messages
        ]
        

        self.assertTrue(
            actual_response_message["response"]["shouldEndSession"]
        )

