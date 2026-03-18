from database.model import Hotels
from datetime import datetime

"""
CRUD operations for the Hotels table.
This module handles direct interaction with the database records.
"""

def store_data(search_user_id: int,
               search_date: datetime,
               search_url: str,
               search_hotel_title: str,
               search_hotel_price: float,
               search_hotel_photos: str,
               search_hotel_coordinates: str) -> None:
    """
    Creates and saves a new hotel search record into the database.

    Args:
        search_user_id (int): ID of the Telegram user.
        search_date (datetime): Timestamp of the search.
        search_url (str): Booking.com link to the hotel.
        search_hotel_title (str): Hotel name.
        search_hotel_price (float): Nightly price.
        search_hotel_photos (str): URL of the main hotel image.
        search_hotel_coordinates (str): GPS coordinates (lat, lon).
    """


    insert_to_database = Hotels(search_user_id=search_user_id,
                                search_date=search_date,
                                search_url=search_url,
                                search_hotel_title=search_hotel_title,
                                search_hotel_price=search_hotel_price,
                                search_hotel_photos=search_hotel_photos,
                                search_hotel_coordinates=search_hotel_coordinates
                                )
    insert_to_database.save()


def retrieve_data(user_id):
    return Hotels.select().where(Hotels.search_user_id == user_id)
