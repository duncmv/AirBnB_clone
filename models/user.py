#!/usr/bin/env python3
"""The models User module"""
from models.base_model import BaseModel


class User(BaseModel):
    """The User class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
