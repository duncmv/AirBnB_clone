#!/usr/bin/python3
"""defines a BaseModel class"""


from datetime import datetime
import os.path
import uuid


class BaseModel:
    """will be the base model for all others"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """str representation of the object"""
        return f"""[{self.__class__.__name__}] ({self.id}) {self.__dict__}"""

    def save(self):
        """updates the updated_at attr"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing
        all keys/values of __dict__"""
        dic = self.__dict__.copy()
        dic['__class__'] = self.__class__.__name__
        dic['created_at'] = dic['created_at'].isoformat()
        dic['updated_at'] = dic['updated_at'].isoformat()
        return dic