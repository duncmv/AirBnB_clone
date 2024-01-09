#!/usr/bin/env python3
"""Models city module"""
from models.base_model import BaseModel


class City(BaseModel):
    """The City class"""
    name = ""
    state_id = ""  # will be State.id
