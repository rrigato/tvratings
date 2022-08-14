from copy import deepcopy
from unittest.mock import MagicMock, patch

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
        """Happy Path ResponseSuccess returns list of TelevisionRating"""
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
    def test_get_one_night_ratings_response_failure(self, load_one_date_mock):
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


    @patch("tvratings.entry.externals_entry.load_one_year")
    def test_year_ratings_summary(self, load_one_year_mock: MagicMock):
        """Unhappy Path repo layer error results in ResponseFailure"""
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.entities.entity_model import YearRatingSummary
        from tvratings.entry.externals_entry import year_ratings_summary
        
        mock_rating_year = 2014
        load_one_year_mock.return_value = (
            get_mock_television_ratings(10), None    
        )

        tv_ratings_summary = year_ratings_summary(mock_rating_year)


        self.assertIsInstance(tv_ratings_summary, YearRatingSummary)
        
        
        [
            self.assertIsNotNone(getattr(
                tv_ratings_summary, attr_name)
            ) 
            for attr_name in dir(tv_ratings_summary)
            if not attr_name.startswith("_")
        ]


    @patch("tvratings.entry.externals_entry.load_one_year")
    def test_year_ratings_summary_unexpected_error(self, 
        load_one_year_mock: MagicMock):
        """Unhappy Path repo layer error results in ResponseFailure"""
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.entry.response_objects import ResponseFailure
        from tvratings.entry.externals_entry import year_ratings_summary
        
        mock_rating_year = 2014
        mock_error_message = "Unexpected ratings retrieval error"
        '''TODO - 
            Pipe back manual component test feedback once 
            repo.load_one_year works
        '''
        load_one_year_mock.return_value = (
            None, mock_error_message
        )

        tv_ratings_summary = year_ratings_summary(mock_rating_year)

        self.assertIsInstance(tv_ratings_summary, ResponseFailure)


    def test_valid_year(self):
        """return valid value or error message"""
        from datetime import datetime
        from fixtures.ratings_fixtures import mock_year_high_low_intent
        from tvratings.entry.externals_entry import valid_year

        
        mock_input_dates = [
            {
                "mock_year": 1997,
                "error_type": str
            },
            {
                "mock_year": 2011,
                "error_type": str
            },
            {
                "mock_year": datetime.today().year + 1,
                "error_type": str
            },
            {
                "mock_year": datetime.today().year + 1000,
                "error_type": str
            },
            {
                "mock_year": datetime.today().year,
                "error_type": type(None)
            },
            {
                "mock_year": 2012,
                "error_type": type(None)
            }
            
        ]
        for mock_input_date in mock_input_dates:
            with self.subTest(mock_input_date=mock_input_date):


                clean_valid_year, invalid_year_error_message = valid_year(
                    mock_input_date["mock_year"]
                )


                if mock_input_date["error_type"] == type(None):
                    self.assertEqual(
                        clean_valid_year,
                        mock_input_date["mock_year"]
                    )

                self.assertIsInstance(
                    invalid_year_error_message,
                    mock_input_date["error_type"]
                )

                