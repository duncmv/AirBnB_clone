#!/usr/bin/env python3
"""Models review module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """The Review class"""
    place_id = ""  # will be Place.id
    user_id = ""  # will be User.id
    text = ""
