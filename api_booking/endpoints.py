import requests
from config_data.config import API_HEADERS, API_URLS
from typing import Dict
from datetime import date, timedelta

"""
Module for handling API requests to Booking.com via RapidAPI.
Each function targets a specific endpoint to retrieve location, filter, or hotel data.
"""

def search_destination(data: Dict,
                       endpoint_url: str = API_URLS['search_destination'],
                       headers: Dict = API_HEADERS) -> requests.Response:
    """
    Fetches the destination ID for a specific city and country.

    Args:
        data (Dict): Dictionary containing 'city' and 'country' keys.
    Returns:
        requests.Response: API response containing destination details (dest_id).
    """
    params = {"query": data['city'] + ', ' + data['country']}

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response


def get_filter(data: Dict,
               endpoint_url: str = API_URLS['get_filter'],
               headers: Dict = API_HEADERS) -> requests.Response:
    """
    Retrieves available filters (like districts/neighborhoods) for a given destination.
    Uses a 1-day dummy range (today to tomorrow) just to fetch static filters.

    Args:
        data (Dict): Dictionary containing 'destination_id'.
    Returns:
        requests.Response: API response with available filters for the location.
    """

    params = {"dest_id": data['destination_id'],
              "search_type": "CITY",
              "arrival_date": date.today(),
              "departure_date": date.today() + timedelta(days=1)}

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response


def search_hotels(data: Dict, sort_type,
                  endpoint_url: str = API_URLS['search_hotels'],
                  headers: Dict = API_HEADERS) -> requests.Response:
    """
    Performs the main hotel search based on user-defined criteria.

    Args:
        data (Dict): Collected user data (dates, budget, district).
        sort_type (str): Sorting method (e.g., price_asc, distance_from_search, etc.).
    Returns:
        requests.Response: API response with a list of hotels matching the filters.
    """

    params = {"dest_id": data['destination_id'],
              "search_type": "CITY",
              "categories_filter": data['district_id'],
              "arrival_date": data['arrival_date'].strftime("%Y-%m-%d"),
              "departure_date": str(data['departure_date']),
              "price_min": data['price_min'],
              "price_max": data['price_max'],
              "sort_by": sort_type,
              "currency_code": "EUR"}

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response


def get_hotel_details(data: Dict, hotel: Dict,
                      endpoint_url: str = API_URLS['get_hotel_details'],
                      headers: Dict = API_HEADERS) -> requests.Response:
    """
    Fetches detailed information for a specific hotel, including its exact location.

    Args:
        data (Dict): User session data (for check-in/out dates).
        hotel (Dict): Dictionary containing the specific 'hotel_id'.
    Returns:
        requests.Response: API response with deep details of the hotel.
    """

    params = {"hotel_id": hotel['hotel_id'],
              "arrival_date": data['arrival_date'].strftime("%Y-%m-%d"),
              "departure_date": data['departure_date'].strftime("%Y-%m-%d"),
              "currency_code": "EUR"}

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response


def get_hotel_photo(hotel: Dict,
                    endpoint_url: str = API_URLS['get_hotel_photos'],
                    headers: Dict = API_HEADERS) -> requests.Response:
    """
    Retrieves a list of image URLs for a specific hotel.

    Args:
        hotel (Dict): Dictionary containing the 'hotel_id'.
    Returns:
        requests.Response: API response with image metadata and URLs.
    """

    params = {"hotel_id": hotel['hotel_id']}

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response
