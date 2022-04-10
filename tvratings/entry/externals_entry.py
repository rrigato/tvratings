from tvratings.entry.input_valdiators import validate_iso_8601_date 
from tvratings.entry.request_objects import ValidRequest 
from tvratings.entry.request_objects import InvalidRequest 

import logging

def get_valid_date(tvratings_day):
    """Request object for invoking an interface that requires a datetime.date input

        Parameters
        ----------
        tvratings_day: str
            ISO 8601 YYYY-MM-DD format

        Returns
        -------
        valid_date_request: ValidRequest or InvalidRequest
            ValidRequest with request_filters
            {
                ratings_date: datetime.date
            }
            or InvalidRequest
    """
    logging.info("get_valid_date - beginning input validation")
    valid_date, date_parse_error = validate_iso_8601_date(iso_formatted_str=tvratings_day)
    
    if date_parse_error is not None:
        logging.info("get_valid_date - InvalidRequest returned")
        return(InvalidRequest(error_message=date_parse_error))

    logging.info("get_valid_date - ValidRequest returned")
    
    return(ValidRequest(request_filters={"ratings_date": valid_date}))
