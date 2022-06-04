from copy import deepcopy
from unittest.mock import patch
from unittest.mock import MagicMock
import unittest


class TestTvratingsBackend(unittest.TestCase):

    @patch("boto3.resource")
    def test_load_one_date(self, boto3_resource_mock):
        """Happy Path dynamodb call succeeds"""
        from datetime import date
        from fixtures.ratings_fixtures import fake_dynamodb_query_response
        from tvratings.entities.entity_model import TelevisionRating
        from tvratings.repo.tvratings_backend import load_one_date
        
        mock_rating_night = date(2014, 1, 4)
        mock_num_time_slots = [0, 3, 5]

        for mock_num_time_slot in mock_num_time_slots:
            with self.subTest(mock_num_time_slot=mock_num_time_slot):

                boto3_resource_mock.return_value.Table.return_value.query.return_value = ( 
                    fake_dynamodb_query_response(
                        mock_num_time_slot
                    )
                )
                television_ratings_entities, ratings_retrieval_error = load_one_date(mock_rating_night)

                for tv_show in television_ratings_entities:
                    self.assertIsInstance(tv_show, TelevisionRating)

                self.assertEqual(len(television_ratings_entities), 
                    mock_num_time_slot,
                    msg=( "\n\n load_one_date is not returning the same number of " + 
                    "TelevisionRating entities as Items returns from DynamoDB")
                )
                self.assertIsNone(ratings_retrieval_error)

    

