from copy import deepcopy
import unittest

@unittest.skip("TODO - implement")
class TestExternalsEntry(unittest.TestCase):
    def test_get_valid_date_request(self):
        """Happy Path ValidRequest returned for a requested date"""
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
                # self.assertEqual(
                #     type(valid_date_request.request_filters["ratings_date"]),
                #     date
                # )


    @unittest.skip("test_get_valid_date_request_bad_input")
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
