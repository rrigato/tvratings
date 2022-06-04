from boto3.dynamodb.conditions import Key
from datetime import date
from fixtures.ratings_fixtures import get_mock_television_ratings
from typing import Union
from tvratings.entities.entity_model import TelevisionRating

import boto3
import logging
import os


def _convert_dynamodb_query_to_entity(dynamodb_items: list) -> None:
    """Converts DynamoDB external query to list of TelevisionRating entities
    """
    logging.info("_convert_dynamodb_query_to_entity - invocation begin")

    for dynamodb_item in dynamodb_items:
        tv_show = TelevisionRating()

        tv_show.show_air_date = dynamodb_item.get("RATINGS_OCCURRED_ON")
        tv_show.time_slot = dynamodb_item.get("TIME")
        tv_show.show_name = dynamodb_item.get("SHOW")
        tv_show.household = dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS")
        tv_show.household_18_49 = dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS_AGE_18_49")
        tv_show.rating = dynamodb_item.get("TOTAL_VIEWERS")
        tv_show.rating_18_49 = dynamodb_item.get("TOTAL_VIEWERS_AGE_18_49")

    logging.info("_convert_dynamodb_query_to_entity - invocation end")

    return(None)


def load_one_date(ratings_occurred_on: date) -> tuple[Union[list[TelevisionRating], None], 
    Union[str, None]]:
    """Loads all television ratings for one saturday night

        Parameters
        ----------
        ratings_occurred_on: datetime.date
            Saturday night ratings date

        Returns
        -------
        television_ratings: list
            Each element is a TelevisionRating entity
            No matching ratings for ratings_occurred_on returns []
            Any unexpected processing errors returns None

        unexpected_error: None
            str if unable to load the television ratings from persistent storage 
    """
    dynamodb_table = boto3.resource("dynamodb", os.environ.get("AWS_REGION")).Table(
        "prod_toonami_ratings"
    )


    return(dynamodb_table.query(
        KeyConditionExpression=Key("RATINGS_OCCURRED_ON").eq(ratings_occurred_on.isoformat())
    ), None)
    