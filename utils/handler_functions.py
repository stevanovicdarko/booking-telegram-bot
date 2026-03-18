from typing import Tuple, Any
import requests
import datetime

"""
Utility functions for input validation and data parsing.
These helpers ensure that user-provided data is clean before being sent to the API or Database.
"""

def is_valid_city_or_state_name(name: str) -> bool:
    """
    Checks if the provided name contains only letters and spaces.
    Prevents numbers or special characters from being sent to location APIs.
    """

    return all(c.isalpha() or c.isspace() for c in name)


def parse_price_range(price_range: str) -> Tuple[Any, Any]:
    """
    Splits a user string like '50 - 100' into two separate values.

    Returns:
       tuple: (min_price, max_price) if format is correct, else (False, False).
    """


    try:
        price_min = price_range.split('-')[0].strip()
        price_max = price_range.split('-')[1].strip()
    except IndexError:
        return False, False
    else:
        return price_min, price_max


def is_connection_ok(request: requests.Response) -> bool:
    """
    Verifies if the API request was successful (HTTP 200 OK).

    Args:
        request (requests.Response): The response object received from the requests library.

    Returns:
        bool: True if status_code is 200 (OK), False otherwise.
    """

    if request.status_code != 200:
        return False
    else:
        return True


def format_date(date: str) -> Any:
    """
    Attempts to convert a string into a datetime object.

    Args:
        date_str (str): Date in DD.MM.YYYY format.
    Returns:
        date object if valid, False otherwise.
    """

    try:
        arrival_date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
    except ValueError:
        return False
    else:
        return arrival_date


def is_all_digit(string_1: str, string_2: str) -> bool:
    """
    Ensures that both provided strings are purely numeric.
    Used for final validation of price inputs before API calls.

    Args:
        string_1 (str): The first string to validate (e.g., min price).
        string_2 (str): The second string to validate (e.g., max price).

    Returns:
        bool: True if both strings are numeric, False if either contains non-digits.
    """

    return string_1.isdigit() and string_2.isdigit()
