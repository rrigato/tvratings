from unittest.mock import MagicMock
from unittest.mock import patch
import unittest


class TestTvratingsBackend(unittest.TestCase):

    @patch("boto3.resource")
    def test_load_one_date(self, boto3_resource_mock):
        """Happy Path dynamodb call succeeds"""
        from datetime import date
        from fixtures.ratings_fixtures import fake_dynamodb_query_response
        from tvratings.entities.entity_model import television_rating_attribute_names
        from tvratings.entities.entity_model import TelevisionRating
        from tvratings.repo.tvratings_backend import load_one_date
        
        mock_rating_night = date(2014, 1, 4)
        mock_num_time_slots = [0, 1, 3, 5]

        for mock_num_time_slot in mock_num_time_slots:
            with self.subTest(mock_num_time_slot=mock_num_time_slot):

                boto3_resource_mock.return_value.Table.return_value.query.return_value = ( 
                    fake_dynamodb_query_response(
                        mock_num_time_slot
                    )
                )


                television_ratings_entities, ratings_retrieval_error = load_one_date(
                    mock_rating_night)


                for tv_show in television_ratings_entities:
                    self.assertIsInstance(tv_show, TelevisionRating)

                    [
                        self.assertIsNotNone(getattr(tv_show, attr_name),
                            msg=f"\n\n {attr_name} not populated in returned entity list"
                        )
                        for attr_name in television_rating_attribute_names()
                    ]

                    
                self.assertEqual(len(television_ratings_entities), 
                    mock_num_time_slot,
                    msg=( "\n\n load_one_date is not returning the same number of " + 
                    "\nTelevisionRating entities as Items returns from DynamoDB")
                )
                self.assertIsNone(ratings_retrieval_error)


    @patch("boto3.resource")
    def test_load_one_date_underlying_table_structure_changes(self, boto3_resource_mock):
        """Key names in underlying Dynamodb table change resulting in an error_message"""
        from datetime import date
        from fixtures.ratings_fixtures import fake_dynamodb_query_response
        from tvratings.repo.tvratings_backend import load_one_date
        
        mock_rating_night = date(2014, 1, 4)
        mock_num_time_slot = 1
        required_keys = ["TIME", "SHOW", "TOTAL_VIEWERS"]

        for required_key in required_keys:
            with self.subTest(required_key=required_key):
                
                dynamodb_item_missing_key_field = fake_dynamodb_query_response(mock_num_time_slot)
                dynamodb_item_missing_key_field["Items"][0].pop(required_key)
                boto3_resource_mock.return_value.Table.return_value.query.return_value = ( 
                    dynamodb_item_missing_key_field
                )


                television_ratings_entities, ratings_retrieval_error = load_one_date(mock_rating_night)


                self.assertIsInstance(ratings_retrieval_error, str)
                self.assertIsNone(television_ratings_entities)


    @patch("boto3.resource")
    def test_load_one_year(self, 
        boto3_resource_mock: MagicMock):
        """Load one year of TelevisionRating Entities"""
        from fixtures.ratings_fixtures import fake_dynamodb_query_response
        from tvratings.entities.entity_model import TelevisionRating
        from tvratings.repo.tvratings_backend import load_one_year

        mock_num_ratings = 52
        mock_ratings_year = 2014
        boto3_resource_mock.return_value.Table.return_value.query.return_value = (
            fake_dynamodb_query_response(mock_num_ratings)
        )


        valid_tv_ratings, ratings_retrieval_error = load_one_year(
            mock_ratings_year
        )


        self.assertIsNone(ratings_retrieval_error)
        self.assertEqual(len(valid_tv_ratings), mock_num_ratings)
        for tv_rating in valid_tv_ratings:
            self.assertIsInstance(tv_rating, TelevisionRating)
        
        args, kwargs = boto3_resource_mock.return_value.Table.return_value.query.call_args
        self.assertEqual(kwargs["IndexName"], "YEAR_ACCESS")
        self.assertIsNotNone(kwargs["KeyConditionExpression"])
        

    @patch("boto3.resource")
    def test_load_one_year_unexpected_error(self, 
        boto3_resource_mock: MagicMock):
        """Boto3 throws runtime error"""
        from tvratings.repo.tvratings_backend import load_one_year
        

        mock_error_message = "simulate boto3 client error"
        boto3_resource_mock.return_value.Table.return_value.query.side_effect = RuntimeError(
            mock_error_message
        )
        mock_ratings_year = 2014
        

        valid_tv_ratings, ratings_retrieval_error = load_one_year(
            mock_ratings_year
        )
        
        
        self.assertIsNone(valid_tv_ratings)
        self.assertIsInstance(ratings_retrieval_error, str)

        