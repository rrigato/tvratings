from copy import deepcopy
import unittest

class TestExternalsEntry(unittest.TestCase):
    def test_get_valid_date_request(self):
        """Happy Path ValidRequest returned for a requested date"""
        from tvratings.entry.externals_entry import get_valid_date
        from tvratings.entry.request_objects import ValidRequest


        mock_input_dates = [
            {"arg1": ["a", "list"]},
            {},
            None,
            {"arg1": 1, "arg2": 2}
        ]
        for mock_input_date in mock_input_dates:
            with self.subTest(mock_input_date=mock_input_date):

                valid_date_request = ValidRequest(request_filters=deepcopy(mock_input_date))

                self.assertEqual(type(valid_date_request), ValidRequest)
