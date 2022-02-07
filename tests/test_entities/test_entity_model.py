from copy import deepcopy
import unittest

class TestEntityModel(unittest.TestCase):
    def test_television_rating(self):
        """TelevisionRating entity created"""
        from tvratings.entities.entity_model import TelevisionRating
        from datetime import date

        mock_burn_day = "3005-11-29"
        mock_television_rating = "Burning Discouraged"
        mock_zip_code = 20002
        mock_air_quality_index = 79
        mock_fine_particulate_matter_2_5 = 24.4
        mock_coarse_particulate_matter_10 = 111


        television_rating_entity = TelevisionRating()


        television_rating_entity.burn_day = date.fromisoformat(mock_burn_day)
        television_rating_entity.television_rating = mock_television_rating
        television_rating_entity.zip_code = mock_zip_code
        television_rating_entity.air_quality_index = mock_air_quality_index
        television_rating_entity.fine_particulate_matter_2_5 = mock_fine_particulate_matter_2_5
        television_rating_entity.coarse_particulate_matter_10 = mock_coarse_particulate_matter_10
        

        self.assertEqual(television_rating_entity.burn_day.isoformat(), mock_burn_day)
        self.assertEqual(television_rating_entity.television_rating, mock_television_rating)
        self.assertEqual(television_rating_entity.zip_code, mock_zip_code)
        self.assertEqual(television_rating_entity.air_quality_index, mock_air_quality_index)
        self.assertEqual(
            television_rating_entity.fine_particulate_matter_2_5, 
            mock_fine_particulate_matter_2_5
        )
        self.assertEqual(
            television_rating_entity.coarse_particulate_matter_10, 
            mock_coarse_particulate_matter_10
        )



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
                    mock_television_rating.burn_day = mock_invalid_type

                with self.assertRaises(TypeError):
                    mock_television_rating.television_rating = mock_invalid_type


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
                    mock_television_rating.zip_code = mock_invalid_type
                
                with self.assertRaises(TypeError):
                    mock_television_rating.air_quality_index = mock_invalid_type

                with self.assertRaises(TypeError):
                    mock_television_rating.fine_particulate_matter_2_5 = mock_invalid_type

                with self.assertRaises(TypeError):
                    mock_television_rating.coarse_particulate_matter_10 = mock_invalid_type


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