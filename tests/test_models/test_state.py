#!/usr/bin/env python3
"""Models state test module"""
from models.state import State
from models.base_model import BaseModel
import unittest


class TestStateClass(unittest.TestCase):
    """test for class"""
    def test_is_subclass(self):
        """test for a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name(self):
        """test for the state_id attr"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        self.assertEqual(state.name, "")

    def test_to_dict_values(self):
        """test the values in dict"""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        state = State()
        new_dict = state.to_dict()
        self.assertEqual(new_dict["__class__"], "State")
        self.assertEqual(type(new_dict['created_at']), str)
        self.assertEqual(type(new_dict['updated_at']), str)
        self.assertEqual(new_dict['created_at'],
                         state.created_at.strftime(time))
        self.assertEqual(new_dict['updated_at'],
                         state.updated_at.strftime(time))

    def test_str(self):
        """test for output str method"""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))
