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
        """Happy Path"""
        from datetime import date
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.entry.externals_entry import get_one_night_ratings
        from tvratings.entry.request_objects import ValidRequest
        from tvratings.entry.response_objects import ResponseSuccess


        mock_television_ratings = get_mock_television_ratings(number_of_ratings=6)
        load_one_date_mock.return_value = (deepcopy(mock_television_ratings), None)


        get_one_night_ratings()