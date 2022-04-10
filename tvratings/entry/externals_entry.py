import logging

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

