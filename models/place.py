#!/usr/bin/env python3
"""Models place module"""
from models.base_model import BaseModel


class Place(BaseModel):
    """The Place class"""
    city_id = ""  # will be City.id
    user_id = ""  # will be User.id
    name = ""
    description = ""
    number_rooms = 0  # int
    number_bathrooms = 0  # int
    max_guest = 0  # int
    price_by_night = 0  # int
    latitude = 0.0  # float
    longitude = 0.0  # float
    amenity_ids = []  # list of strings
