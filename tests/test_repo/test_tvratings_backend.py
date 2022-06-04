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
        from tvratings.repo.tvratings_backend import load_one_date
        
        mock_rating_night = date(2014,1,4)
        mock_num_time_slots = 0

        boto3_resource_mock.return_value.Table.return_value = fake_dynamodb_query_response(
            mock_num_time_slots
        )

        television_ratings_entities, ratings_retrieval_error = load_one_date(mock_rating_night)

        self.assertIsInstance(television_ratings_entities, list)
        self.assertIsNone(ratings_retrieval_error)

    

