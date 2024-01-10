#!/usr/bin/env python3
"""The models User module"""
from models.base_model import BaseModel


class User(BaseModel):
    """The User class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def user_help(arg):
        """Utilizes the docstring of User methods to provide help
        on the command interpreter: HELP USER.ALL, HELP USER

        If no matching method is found, returns True to proceed to
        proceed to the default action
        """

        arr = arg.split(".")  # args[0] is User
        if len(arr) >= 2:
            meth = getattr(User, arr[1], None)
            if not meth:
                return True  # This lets default action proceed
            print(getattr(User, arr[1]).__doc__)
        else:
            print(User.__doc__)

    @staticmethod
    def all(arg):
        """Retrieve all users and print them"""
        from models import storage

        objs = storage.all()
        for key, value in objs.items():
            if key.lower().startswith("user"):
                print(value)
