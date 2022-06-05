from boto3.dynamodb.conditions import Key
from datetime import date
from typing import Union
from tvratings.entities.entity_model import TelevisionRating

import boto3
import logging
import os


def _convert_dynamodb_query_to_entity(dynamodb_items: list) -> list[TelevisionRating]:
    """Converts DynamoDB external query to list of TelevisionRating entities
    """
    logging.info("_convert_dynamodb_query_to_entity - invocation begin")

    all_tvratings = []

    for dynamodb_item in dynamodb_items:
        tv_show = TelevisionRating()

        tv_show.show_air_date = dynamodb_item["RATINGS_OCCURRED_ON"]
        tv_show.time_slot = dynamodb_item["TIME"]
        tv_show.show_name = dynamodb_item["SHOW"]
        tv_show.household = dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS")
        tv_show.household_18_49 = dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS_AGE_18_49")
        tv_show.rating = dynamodb_item["TOTAL_VIEWERS"]
        tv_show.rating_18_49 = dynamodb_item.get("TOTAL_VIEWERS_AGE_18_49")

        all_tvratings.append(tv_show)

    logging.info(f"_convert_dynamodb_query_to_entity - len(all_tvratings) - {len(all_tvratings)}")

    return(all_tvratings)


def load_one_date(ratings_occurred_on: date) -> tuple[Union[list[TelevisionRating], None], 
    Union[str, None]]:
    """Loads all television ratings for one saturday night

        Parameters
        ----------
        ratings_occurred_on
            Saturday night ratings date

        Returns
        -------
        television_ratings
            Each element is a TelevisionRating entity
            No matching ratings for ratings_occurred_on returns []
            Any unexpected processing errors returns None

        unexpected_error
            str if unable to load the television ratings from persistent storage 
    """
    try:    
        dynamodb_table = boto3.resource("dynamodb", os.environ.get("AWS_REGION")).Table(
            "prod_toonami_ratings"
        )

        logging.info("load_one_date - obtained table resource")

        dynamodb_response = dynamodb_table.query(
            KeyConditionExpression=Key("RATINGS_OCCURRED_ON").eq(ratings_occurred_on.isoformat())
        )

        logging.info("load_one_date - obtained dynamodb_response")

        if len(dynamodb_response["Items"]) == 0:
            logging.info("load_one_date - dynamodb_response Items list has no elements")
            return([], None)


        logging.info("load_one_date - invoking _convert_dynamodb_query_to_entity")

        return(_convert_dynamodb_query_to_entity(dynamodb_response["Items"]), None)
        

    except Exception as error_suppression:
        logging.exception("load_one_date - unexpected error")
        return(None, "load_one_date - error while retrieving persisted television_ratings")
