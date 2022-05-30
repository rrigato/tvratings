from datetime import date

import logging


def validate_str_input(str_input, max_len):
    """Confirms input provided from external is a str below max_len

        Parameters
        ----------
        str_input: str
            input that needs to be confirmed as a str

        max_len: int
            maximum number of characters in str_input

        Returns
        -------
        str_validation_error: None
            str if str_input did not pass validation
    """
    if type(str_input) != str:
        return("validate_str_input - incorrect data type")

    if len(str_input) > max_len:
        return("validate_str_input - string exceeds max length")

    return(None)


def validate_iso_8601_date(iso_formatted_str):
    """Confirms that provided input is a str in ISO 8601 YYYY-MM-DD format

        Parameters
        ----------
        iso_formatted_str: str
            ISO 8601 YYYY-MM-DD format

        Returns
        -------
        parsed_date: datetime.date
            iso_formatted_str converted to a date

        str_validation_error: None
            str if input validation did not pass
    """
    if validate_str_input(str_input=iso_formatted_str, max_len=15) is not None:
        return(None, validate_str_input(str_input=iso_formatted_str, max_len=15))

    try:
        return(date.fromisoformat(iso_formatted_str), None)

    except Exception as error_suppression:
        logging.exception("validate_iso_8601_date - date.fromisoformat failed")
        return(None, "validate_iso_8601_date - str input not YYYY-MM-DD formatted")



def validate_numeric_input(numeric_input, min_val, max_val):
    """Validates numeric input is type int/float and in the inclusive interval [min_val, max_val]

        Parameters
        ----------
        numeric_input: int or float
            input that needs to be confirmed as a numeric

        min_val: int or float
            minimum value for numeric input

        max_val: int or float
            maximum for numeric_input

        Returns
        -------
        validation_error: None
            str if numeric_input did not pass validation
    """
    if type(numeric_input) not in (int, float):
        return("validate_numeric_input - incorrect data type")

    if numeric_input < min_val:
        return("validate_numeric_input - numeric_input < min_val")

    if numeric_input > max_val:
        return("validate_numeric_input - numeric_input > max_val")

    return(None)