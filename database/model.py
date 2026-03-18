from peewee import Model, IntegerField, AutoField, DateTimeField, TextField, FloatField
from database.db import db

"""
ORM Models for the Hotel Bot Database.
This module defines the schema for storing user search history.
"""

class Hotels(Model):
    """
    Represents a single hotel search result saved in the database.
    Each record maps to a specific hotel found during a user session.
    """

    search_number = AutoField()
    search_user_id = IntegerField()
    search_date = DateTimeField()
    search_url = TextField()
    search_hotel_title = TextField()
    search_hotel_price = FloatField()
    search_hotel_photos = TextField()
    search_hotel_coordinates = TextField()

    def __str__(self):
        """
        Returns a formatted string representation of the record for easy logging/display.
        """
        return 'Redni br. {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(self.search_number,
                                                                       self.search_user_id,
                                                                       self.search_date,
                                                                       self.search_url,
                                                                       self.search_hotel_title,
                                                                       self.search_hotel_price,
                                                                       self.search_hotel_photos,
                                                                       self.search_hotel_coordinates)


    class Meta:
        database = db


def create_db_and_tabels() -> None:
    """
    Initializes the database and creates the necessary tables if they do not exist.
    """
    db.create_tables([Hotels])
