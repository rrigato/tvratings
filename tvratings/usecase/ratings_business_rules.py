from tvratings.entities.entity_model import TelevisionRating

import logging


def select_highest_ratings(tv_ratings_list: 
    list[TelevisionRating]) -> TelevisionRating:
    """Returns highest TelevisionRating in tv_rating_list
    Assumes tv_ratings_list is populated
    """
    highest_rating: int = max([
        tv_rating.rating for tv_rating in tv_ratings_list
        if tv_rating.rating is not None
    ])

    for tv_rating in tv_ratings_list:
        if tv_rating.rating == highest_rating:
            return(tv_rating)
    

def select_lowest_ratings(tv_ratings_list: 
    list[TelevisionRating]) -> TelevisionRating:
    """Returns lowest TelevisionRating in tv_rating_list
    Assumes tv_ratings_list is populated
    """
    lowest_rating: int = min([
        tv_rating.rating for tv_rating in tv_ratings_list
        if tv_rating.rating is not None
    ])

    for tv_rating in tv_ratings_list:
        if tv_rating.rating == lowest_rating:
            return(tv_rating)


def _check_if_none(tv_ratings_list: 
    list[TelevisionRating]) -> list[TelevisionRating]:
    """"""
    logging.info(f"_check_if_none - {len(tv_ratings_list)}")
    return([
        tv_rating for tv_rating in tv_ratings_list
        if tv_rating.rating is not None
    ])


def _check_below_min(tv_ratings_list: 
    list[TelevisionRating]) -> list[TelevisionRating]:
    """"""
    logging.info(f"_check_below_min - {len(tv_ratings_list)}")
    return([
        tv_rating for tv_rating in tv_ratings_list
        if tv_rating.rating >= 5
    ])


def _check_above_max(tv_ratings_list: 
    list[TelevisionRating]) -> list[TelevisionRating]:
    """"""
    logging.info(f"_check_above_max - {len(tv_ratings_list)}")
    return([
        tv_rating for tv_rating in tv_ratings_list
        if tv_rating.rating < 10000
    ])


def filter_by_rating(tv_ratings_list: 
    list[TelevisionRating]) -> list[TelevisionRating]:
    """Mutates tv_ratings_list to remove any TelevisionRating
    entities with data quality issues for the rating element
    """
    logging.info(f"filter_by_rating - {len(tv_ratings_list)}")

    tv_ratings_list = _check_if_none(tv_ratings_list)

    tv_ratings_list = _check_below_min(tv_ratings_list)

    tv_ratings_list = _check_above_max(tv_ratings_list)

    return(tv_ratings_list)
