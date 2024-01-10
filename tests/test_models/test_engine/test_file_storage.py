#!/usr/bin/env python3
"""The models FileStorage test module"""
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import os
import json
import unittest

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorage(unittest.TestCase):
    """test for FileStorage class"""

    def test_all(self):
        """test for all return the __object attr"""
        strg = FileStorage()
        new_dict = strg.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, strg._FileStorage__objects)

    def test_new(self):
        """test the new add a object"""
        strg = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                strg.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, strg._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    def test_save(self):
        """Test to save object in file.json"""
        os.remove("file.json")
        strg = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        strg.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            jf = f.read()
        self.assertEqual(json.loads(string), json.loads(jf))

    def test_reload(self):
        """Test that reload method loads objects from the JSON file"""
        # Save some objects to the file
        os.remove("file.json")
        strg = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        strg.save()

        new_strg = FileStorage()
        new_strg.reload()
        self.assertEqual(new_strg.all(), new_dict)
        FileStorage._FileStorage__objects = save

    def test_save_changes(self):
        """Test save_changes method"""
        strg = FileStorage()
        obj = list(strg.all().values())[0]  # Get any object
        obj_name = "{}.{}".format(obj.__class__.__name__, obj.id)
        obj.some_attribute = "modified"
        strg.save_changes({obj_name: obj})
        new_strg = FileStorage()
        new_strg.reload()
        self.assertEqual(new_strg.all()[obj_name].some_attribute, "modified")
