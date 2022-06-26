from copy import deepcopy
from unittest.mock import MagicMock
from unittest.mock import patch

import json
import unittest

class TestRatingsNightIntent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/events/intent_requests/ratings_night_intent.json", "r") as intent_request:
            cls.intent_request = json.load(intent_request)


    @patch("externals.alexa_intents.ratings_night_intent.get_one_night_ratings")
    @patch("externals.alexa_intents.ratings_night_intent.get_valid_date")
    def test_ratings_night_intent(self, get_valid_date_mock: MagicMock, 
        get_one_night_ratings_mock: MagicMock):
        """RatingsNightIntentHandler.handle executes succesfully"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.entry.response_objects import ResponseSuccess
        from tvratings.entry.request_objects import ValidRequest
        
        mock_ratings_ocurred_on = self.intent_request["request"]["intent"]["slots"][
            "rating_occurred_on"]["value"]

        expected_message = "The ratings for that Saturday night were"
        mock_television_ratings = get_mock_television_ratings(7)

        get_valid_date_mock.return_value = ValidRequest(request_filters={
            "ratings_date": mock_ratings_ocurred_on
        })
        get_one_night_ratings_mock.return_value = ResponseSuccess(
            response_value=mock_television_ratings
        )

        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )


        self.assertTrue(get_valid_date_mock.assert_called)

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
    def test_ratings_night_intent_unexpected_error(self, entry_intent_handler):
        """RatingsNightIntentHandler.handle raises unexpected errror that is handled gracefully"""
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler

        alexa_lambda_handler = get_alexa_lambda_handler()

        entry_intent_handler.side_effect = TimeoutError("Unexpected Network timeout")

        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )

        self.assertEqual(type(actual_response_message["response"]["outputSpeech"]["ssml"]), str)
    
        self.assertTrue(actual_response_message["response"]["shouldEndSession"])




    @patch("externals.alexa_intents.ratings_night_intent.get_one_night_ratings")
    @patch("externals.alexa_intents.ratings_night_intent.get_valid_date")
    def test_ratings_night_intent_e2e_bugs(self, get_valid_date_mock: MagicMock, 
        get_one_night_ratings_mock: MagicMock):
        """E2E bugs: 
            - passing datetime.date to get_one_night_ratings instead of ValidRequest object
        """
        from externals.alexa_intents.intent_dispatcher import get_alexa_lambda_handler
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.entry.response_objects import ResponseSuccess
        from tvratings.entry.request_objects import ValidRequest
        
        mock_ratings_ocurred_on = self.intent_request["request"]["intent"]["slots"][
            "rating_occurred_on"]["value"]

        mock_num_ratings = 10
        mock_television_ratings = get_mock_television_ratings(mock_num_ratings)

        get_valid_date_mock.return_value = ValidRequest(request_filters={
            "ratings_date": mock_ratings_ocurred_on
        })
        get_one_night_ratings_mock.return_value = ResponseSuccess(
            response_value=mock_television_ratings
        )

        alexa_lambda_handler = get_alexa_lambda_handler()


        actual_response_message = alexa_lambda_handler(
            deepcopy(self.intent_request), 
            None
        )

        args, kwargs = get_one_night_ratings_mock.call_args
        self.assertIsInstance(
            args[0], ValidRequest, msg="""\n\n
                Not passing a ValidRequest object to entry interface
            """
        )

        self.assertEqual(
            actual_response_message["response"]["outputSpeech"]["ssml"].count("thousand viewers."),
            mock_num_ratings,
            msg="""\n\n Error do not have one description for each television rating"""
        )

