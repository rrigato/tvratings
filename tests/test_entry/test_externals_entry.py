from copy import deepcopy
from unittest.mock import patch

import unittest


class TestExternalsEntry(unittest.TestCase):
    def test_get_valid_date_request(self):
        """Happy Path ValidRequest returned on valid YYYY-MM-DD formatted input"""
        from datetime import date
        from tvratings.entry.externals_entry import get_valid_date
        from tvratings.entry.request_objects import ValidRequest


        mock_input_dates = [
            "3005-11-28",
            "2050-06-01",
            "2005-11-28",
            "2000-01-01"
        ]
        for mock_input_date in mock_input_dates:
            with self.subTest(mock_input_date=mock_input_date):

                valid_date_request = get_valid_date(tvratings_day=mock_input_date)

                self.assertEqual(type(valid_date_request), ValidRequest)
                self.assertEqual(
                    type(valid_date_request.request_filters["ratings_date"]),
                    date
                )


    def test_get_valid_date_request_bad_input(self):
        """Unhappy Path, input format is not YYYY-MM-DD"""
        from tvratings.entry.externals_entry import get_valid_date
        from tvratings.entry.request_objects import InvalidRequest


        mock_input_dates = [
            "3005/11/28",
            "not_a_date",
            100,
            12.21,
            [],
            {}
        ]
        for mock_input_date in mock_input_dates:
            with self.subTest(mock_input_date=mock_input_date):

                valid_date_request = get_valid_date(tvratings_day=mock_input_date)

                self.assertEqual(type(valid_date_request), InvalidRequest)
                self.assertEqual(type(valid_date_request.error_message), str)

    @patch("tvratings.entry.externals_entry.load_one_date")
    def test_get_one_night_ratings(self, load_one_date_mock):
        """Happy Path ResponseSuccess of TelevisionRating returned"""
        from datetime import date
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.entities.entity_model import TelevisionRating
        from tvratings.entry.externals_entry import get_one_night_ratings
        from tvratings.entry.request_objects import ValidRequest

        mock_input_date = date.fromisoformat("2014-01-04")
        mock_television_ratings = get_mock_television_ratings(number_of_ratings=6)
        load_one_date_mock.return_value = (deepcopy(mock_television_ratings), None)


        one_nights_ratings = get_one_night_ratings(valid_date_request=ValidRequest(
                request_filters={"ratings_date": mock_input_date}
            )
        )


        [
            self.assertEqual(type(rating), TelevisionRating) 
            for rating in one_nights_ratings.response_value
        ]
        self.assertEqual(len(mock_television_ratings), len(one_nights_ratings.response_value))


    @patch("tvratings.entry.externals_entry.load_one_date")
    def test_get_one_night_ratings(self, load_one_date_mock):
        """Unhappy Path repo layer error results in ResponseFailure"""
        from datetime import date
        from tvratings.entry.externals_entry import get_one_night_ratings
        from tvratings.entry.request_objects import ValidRequest

        mock_input_date = date.fromisoformat("2014-01-04")
        mock_error_message = "Botocore: table name not found"
        load_one_date_mock.return_value = (None, mock_error_message)


        one_nights_ratings = get_one_night_ratings(valid_date_request=ValidRequest(
                request_filters={"ratings_date": mock_input_date}
            )
        )


        
        self.assertEqual(str, type(one_nights_ratings.error_message))
        self.assertFalse(one_nights_ratings)

