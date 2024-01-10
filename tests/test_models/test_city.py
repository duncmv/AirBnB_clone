#!/usr/bin/env python3
"""Models city test module"""
from models.city import City
from models.base_model import BaseModel
import unittest


class TestCityClass(unittest.TestCase):
    """test for class"""
    def test_is_subclass(self):
        """test for a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_state_id(self):
        """thest for for attribute state id for City class"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        self.assertEqual(city.state_id, "")

    def test_name(self):
        """test for the state_id attr"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        self.assertEqual(city.name, "")

    def test_to_dict_values(self):
        """test the values in dict"""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        city = City()
        new_dict = city.to_dict()
        self.assertEqual(new_dict["__class__"], "City")
        self.assertEqual(type(new_dict['created_at']), str)
        self.assertEqual(type(new_dict['updated_at']), str)
        self.assertEqual(new_dict['created_at'],
                         city.created_at.strftime(time))
        self.assertEqual(new_dict['updated_at'],
                         city.updated_at.strftime(time))

    def test_str(self):
        """test for output str method"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))
