import unittest

class TestEntityModel(unittest.TestCase):
    def test_television_rating(self):
        """TelevisionRating entity created"""
        from tvratings.entities.entity_model import TelevisionRating
        from datetime import date

        mock_show_air_date = "2014-01-04"
        mock_timeslot = "12:00"
        mock_show_name = "Bleach"
        mock_rating = 1084
        mock_rating_18_49 = None
        mock_household = .8
        mock_household_18_49 = None


        television_rating_entity = TelevisionRating()


        television_rating_entity.show_air_date = date.fromisoformat(mock_show_air_date)
        television_rating_entity.timeslot = mock_timeslot
        television_rating_entity.show_name = mock_show_name
        television_rating_entity.rating = mock_rating
        television_rating_entity.rating_18_49 = mock_rating_18_49
        television_rating_entity.household = mock_household
        television_rating_entity.household_18_49 = mock_household_18_49
        

        self.assertEqual(television_rating_entity.show_air_date.isoformat(), mock_show_air_date)
        self.assertEqual(television_rating_entity.timeslot, mock_timeslot)
        self.assertEqual(television_rating_entity.show_name, mock_show_name)
        self.assertEqual(television_rating_entity.rating, mock_rating)
        self.assertEqual(television_rating_entity.rating_18_49, mock_rating_18_49)
        self.assertEqual(television_rating_entity.household, mock_household)
        self.assertEqual(television_rating_entity.household_18_49, mock_household_18_49)



    def test_television_rating_bad_input_str_attributes(self):
        """TelevisionRating str attributes passed invalid input raises TypeError"""
        from tvratings.entities.entity_model import TelevisionRating

        mock_invalid_types = [
            set(["a", "b"]),
            3005,
            11.29,
            (1, 2, 3),
            {},
            ["a", "list"]
        ]

        for mock_invalid_type in mock_invalid_types:
            with self.subTest(mock_invalid_type=mock_invalid_type):

                mock_television_rating = TelevisionRating()
                
                with self.assertRaises(TypeError):
                    mock_television_rating.timeslot = mock_invalid_type

                with self.assertRaises(TypeError):
                    mock_television_rating.show_name = mock_invalid_type


    def test_television_rating_bad_input_numeric_attributes(self):
        """TelevisionRating numeric attributes passed invalid input raises TypeError"""
        from tvratings.entities.entity_model import TelevisionRating

        mock_invalid_types = [
            set(["a", "b"]),
            "3005",
            "11.29",
            (1, 2, 3),
            {},
            ["a", "list"]
        ]

        for mock_invalid_type in mock_invalid_types:
            with self.subTest(mock_invalid_type=mock_invalid_type):

                mock_television_rating = TelevisionRating()

                with self.assertRaises(TypeError):
                    mock_television_rating.rating = mock_invalid_type
                
                with self.assertRaises(TypeError):
                    mock_television_rating.rating_18_49 = mock_invalid_type

                with self.assertRaises(TypeError):
                    mock_television_rating.household = mock_invalid_type

                with self.assertRaises(TypeError):
                    mock_television_rating.household_18_49 = mock_invalid_type


    def test_television_rating_defaults_none(self):
        """All TelevisionRating attributes are None after instance intialization"""
        from tvratings.entities.entity_model import TelevisionRating

        television_rating_entity = TelevisionRating()

        
        television_rating_attributes = [
            attribute_name for attribute_name in dir(television_rating_entity) 
            if not attribute_name.startswith("_")
        ]

        [
            self.assertIsNone(getattr(television_rating_entity, television_rating_attribute)) 
            for television_rating_attribute in television_rating_attributes
        ]