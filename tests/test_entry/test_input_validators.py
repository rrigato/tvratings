from copy import deepcopy
import unittest

class TestInputValidators(unittest.TestCase):
    def test_validate_str_input(self):
        """Happy Path valid str input"""
        from tvratings.entry.input_valdiators import validate_str_input

        mock_str_inputs = [
            ["A", 1], 
            ["ABCd"*50, 250], 
            ["ABCd_e76", 8]
        ]
        for mock_str_input in mock_str_inputs:
            with self.subTest(mock_str_input=mock_str_input):
                self.assertIsNone(validate_str_input(
                    str_input=mock_str_input[0],
                    max_len=mock_str_input[1]
                ))


    def test_validate_str_input_bad_input(self):
        """Unhappy Path, incorrect data type or string length"""
        from tvratings.entry.input_valdiators import validate_str_input

        mock_str_inputs = [
            ["AB", 1], 
            ["ABCd"*500, 250], 
            [1.2, 10],
            [[], 10],
            [5, 10],
            [None, 10]
        ]

        for mock_str_input in mock_str_inputs:
            with self.subTest(mock_str_input=mock_str_input):
                self.assertEqual(
                    type(
                        validate_str_input(
                            str_input=mock_str_input[0],
                            max_len=mock_str_input[1]
                        )
                    ),
                    str
                )


    def test_validate_iso_8601_date(self):
        """Happy Path valid YYYY-MM-DD input"""
        from tvratings.entry.input_valdiators import validate_iso_8601_date

        mock_str_inputs = [
            "3005-11-29",
            "2000-01-01",
            "2022-06-15",
            "2025-12-25"
        ]
        for mock_str_input in mock_str_inputs:
            with self.subTest(mock_str_input=mock_str_input):
                parsed_date, parse_date_error = validate_iso_8601_date(iso_formatted_str=mock_str_input)

                self.assertIsNone(parse_date_error)
                self.assertEqual(parsed_date.isoformat(), mock_str_input)


    
    def test_validate_iso_8601_date_bad_input(self):
        """Unhappy Path input is not a YYYY-MM-DD str"""
        from tvratings.entry.input_valdiators import validate_iso_8601_date
        from datetime import date

        mock_inputs = [
            "3005/11/29",
            "01-01-2025",
            "12/20/2022",
            date.fromisoformat("3005-11-29"),
            {},
            ["not_a_str"]
        ]
        for mock_input in mock_inputs:
            with self.subTest(mock_input=mock_input):
                parsed_date, parse_date_error = validate_iso_8601_date(iso_formatted_str=mock_input)

                self.assertIsNone(parsed_date)
                self.assertEqual(type(parse_date_error), str)


    def test_validate_numeric_input(self):
        """Happy Path, valid numeric input"""
        from tvratings.entry.input_valdiators import validate_numeric_input

        mock_numeric_inputs = [
            [3005, 11, 9000],
            [1.5, 1.0, 2.0],
            [1.3, 1.3, 1.3],
            [3005, 11, 3006],
            [3005, 3004, 3008],
            [3005, 3005, 3005]

        ]

        for mock_numeric_input in mock_numeric_inputs:
            with self.subTest(mock_numeric_input=mock_numeric_input):
                self.assertIsNone(
                    validate_numeric_input(
                        numeric_input=mock_numeric_input[0],
                        min_val=mock_numeric_input[1],
                        max_val=mock_numeric_input[2],
                    )
                    
                )


    def test_validate_numeric_input_bad_input(self):
        """Unhappy Path, incorrect data type or values"""
        from tvratings.entry.input_valdiators import validate_numeric_input

        mock_numeric_inputs = [
            [3005, 11, 28],
            [1.5, 1.0, 1.1],
            [1.2, 1.3, 1.3],
            [3005, 3006, 3007],
            [3005, 3008, 3008],
            
            ["20002", 0, 100000],
            [None, 0, 100000]

        ]

        for mock_numeric_input in mock_numeric_inputs:
            with self.subTest(mock_numeric_input=mock_numeric_input):
                self.assertEqual(
                    type(
                        validate_numeric_input(
                            numeric_input=mock_numeric_input[0],
                            min_val=mock_numeric_input[1],
                            max_val=mock_numeric_input[2],
                        )
                    ),
                    str
                )

                