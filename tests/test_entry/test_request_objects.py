from copy import deepcopy
import unittest

class TestRequestObjects(unittest.TestCase):
    def test_valid_request(self):
        """Happy Path ValidRequest for different request filters"""
        from tvratings.entry.request_objects import ValidRequest


        mock_request_filters = [
            {"arg1": ["a", "list"]},
            {},
            None,
            {"arg1": 1, "arg2": 2}
        ]
        for mock_request_filter in mock_request_filters:
            with self.subTest(mock_request_filter=mock_request_filter):

                mock_request_object = ValidRequest(request_filters=deepcopy(mock_request_filter))

                self.assertEqual(mock_request_filter, mock_request_object.request_filters)
                self.assertTrue(bool(mock_request_object))


    def test_valid_request_bad_input(self):
        """Unhappy Path ValidRequest invalid datatype for request_filters"""
        from tvratings.entry.request_objects import ValidRequest


        mock_request_filters = [
            set(["a", "b"]),
            "arg1", 
            1, 
            2.0,
            (1, 2, 3)
        ]
        for mock_request_filter in mock_request_filters:
            with self.subTest(mock_request_filter=mock_request_filter):

                with self.assertRaises(TypeError):
                    mock_request_object = ValidRequest(request_filters=deepcopy(mock_request_filter))


