from boto3.dynamodb.conditions import Key
from datetime import date
from typing import Union
from tvratings.entities.entity_model import TelevisionRating

import boto3
import logging
import os


def _convert_dynamodb_query_to_entity(dynamodb_items: list[dict]
    ) -> list[TelevisionRating]:
    """Converts DynamoDB external query to list of TelevisionRating entities
    """
    logging.info("_convert_dynamodb_query_to_entity - invocation begin")

    all_tvratings = []

    for dynamodb_item in dynamodb_items:
        tv_show = TelevisionRating()

        tv_show.show_air_date = date.fromisoformat(
            dynamodb_item["RATINGS_OCCURRED_ON"]
        )
        tv_show.time_slot = dynamodb_item["TIME"]
        tv_show.show_name = dynamodb_item["SHOW"]

        if dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS") is not None:
            tv_show.household = float(dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS"))

        if dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS_AGE_18_49") is not None:
            tv_show.household_18_49 = float(dynamodb_item.get("PERCENTAGE_OF_HOUSEHOLDS_AGE_18_49"))
        
        tv_show.rating = int(dynamodb_item["TOTAL_VIEWERS"])

        if dynamodb_item.get("YEAR") is not None:
            tv_show.rating_year = int(dynamodb_item.get("YEAR"))

        if dynamodb_item.get("TOTAL_VIEWERS_AGE_18_49") is not None:
            tv_show.rating_18_49 = int(dynamodb_item.get("TOTAL_VIEWERS_AGE_18_49"))

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
                Attributes guarunteed to be populated per entity:
                    - show_air_date
                    - time_slot
                    - show_name
                    - rating

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

        return(
            _convert_dynamodb_query_to_entity(
                dynamodb_response["Items"]
            ),
            None
        )
        

    except Exception as error_suppression:
        logging.exception("load_one_date - unexpected error")
        return(None, "load_one_date - error while retrieving persisted television_ratings")




def load_one_year(ratings_year: int) -> tuple[
    Union[list[TelevisionRating], None], Union[str, None]]:
    """returns None, error_message if error 
    returns [], None if no ratings found for year
    """
    try:
        dynamodb_table = boto3.resource(
            "dynamodb", 
            os.environ.get("AWS_REGION")
        ).Table(
            "prod_toonami_ratings"
        )

        logging.info("load_one_year - obtained table resource")

        dynamodb_response = dynamodb_table.query(
            IndexName="YEAR_ACCESS",
            KeyConditionExpression=Key("YEAR").eq(ratings_year)
        )

        logging.info("load_one_year - obtained dynamodb_response")

        if len(dynamodb_response["Items"]) == 0:
            logging.info(
                "load_one_year - dynamodb_response Items list empty"
            )
            return([], None)

        return(
            _convert_dynamodb_query_to_entity(
                dynamodb_response["Items"]
            ),
            None
        )


    except Exception as error_suppression:
        logging.exception("load_year_date - unexpected error")
        return(
            None, 
            "load_year_date - error while retrieving television ratings"
        )



if __name__ == "__main__":
    from time import strftime
    import logging
    import os
    os.environ["AWS_REGION"] = "us-east-1"
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s.%(msecs)03d" + strftime("%z") + " | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S", level=logging.INFO
    )
    load_one_year(2014)

