#!/usr/bin/env python3
"""Models amenities test module"""
from models.amenity import Amenity
from models.base_model import BaseModel
import unittest


class TestAmenityClass(unittest.TestCase):
    """test for class"""
    def test_is_subclass(self):
        """test for a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name(self):
        """test for the state_id attr"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        self.assertEqual(amenity.name, "")

    def test_to_dict_values(self):
        """test the values in dict"""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        amenity = Amenity()
        new_dict = amenity.to_dict()
        self.assertEqual(new_dict["__class__"], "Amenity")
        self.assertEqual(type(new_dict['created_at']), str)
        self.assertEqual(type(new_dict['updated_at']), str)
        self.assertEqual(new_dict['created_at'],
                         amenity.created_at.strftime(time))
        self.assertEqual(new_dict['updated_at'],
                         amenity.updated_at.strftime(time))

    def test_str(self):
        """test for output str method"""
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))
