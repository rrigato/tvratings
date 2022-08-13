from copy import deepcopy
import unittest

class TestResponseObjects(unittest.TestCase):
    def test_response_success(self):
        """ResponseSuccess for different datatypes"""
        from tvratings.entry.response_objects import ResponseSuccess


        mock_response_values = [
            {"arg1": ["a", "list"]},
            {},
            None,
            {"arg1": 1, "arg2": 2},
            set(["a", "b"]),
            "arg1", 
            1, 
            2.0,
            (1, 2, 3)

        ]
        for mock_response_value in mock_response_values:
            with self.subTest(mock_response_value=mock_response_value):

                mock_response_object = ResponseSuccess(response_value=deepcopy(mock_response_value))

                self.assertEqual(mock_response_value, mock_response_object.response_value)
                self.assertTrue(bool(mock_response_object))


    def test_response_failure(self):
        """ResponseFailure.error_message passed a str"""
        from tvratings.entry.response_objects import ResponseFailure
        mock_response_message = "mock error message"
        
        mock_response_object = ResponseFailure(error_message=mock_response_message)

        self.assertEqual(mock_response_message, mock_response_object.error_message)
        self.assertFalse(mock_response_object)


    def test_response_failure_bad_input(self):
        """ResponseFailure.error_message not passed a str"""
        from tvratings.entry.response_objects import ResponseFailure


        mock_error_messages = [
            {"arg1": ["a", "list"]},
            {},
            None,
            {"arg1": 1, "arg2": 2},
            set(["a", "b"]),
            1, 
            2.0,
            (1, 2, 3)

        ]
        for mock_error_message in mock_error_messages:
            with self.subTest(mock_error_message=mock_error_message):
                with self.assertRaises(TypeError):
                    mock_response_object = ResponseFailure(error_message=mock_error_message)

