#!/usr/bin/env python3
"""Models user test module"""
from models.user import User
from models.base_model import BaseModel
import unittest


class TestUserClass(unittest.TestCase):
    """test for class"""
    def test_is_subclass(self):
        """test for a subclass of BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email(self):
        """test for email attribute"""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, "")

    def test_password(self):
        """test for password attribute"""
        user = User()
        self.assertTrue(hasattr(user, "password"))
        self.assertEqual(user.password, "")

    def test_first_name(self):
        """test for the first name attribute"""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        self.assertEqual(user.first_name, "")

    def test_last_name(self):
        """test for last name attribute and if is string"""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.last_name, "")

    def test_to_dict_creat(self):
        """test to_dict method create dictionary with correct att"""
        user = User()
        new_dict = user.to_dict()
        self.assertEqual(type(new_dict), dict)
        for attr in user.__dict__:
            self.assertTrue(attr in new_dict)
            self.assertTrue("__class__" in new_dict)

    def test_to_dict_values(self):
        """test the values in dict"""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        user = User()
        new_dict = user.to_dict()
        self.assertEqual(new_dict["__class__"], "User")
        self.assertEqual(type(new_dict['created_at']), str)
        self.assertEqual(type(new_dict['updated_at']), str)
        self.assertEqual(new_dict['created_at'],
                         user.created_at.strftime(time))
        self.assertEqual(new_dict['updated_at'],
                         user.updated_at.strftime(time))

    def test_str(self):
        """test for output str method"""
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))
