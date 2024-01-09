#!/usr/bin/env python3
"""FileStorage module"""
import json
from pathlib import Path


class FileStorage:
    """The FileStorage class"""
    __file_path = "file.json"  # path to the json file
    __objects = {}  # will store all objects by <classname>.id as key

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ;"""
        if not Path(self.__file_path).is_file():
            return
        with open(self.__file_path, "r") as fil:
            self.__objects = json.load(fil)

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        fil = Path(self.__file_path)
        if fil.is_dir() or (not fil.parent.exists()):
            # print("File Path: {}".format(self.__file_path))
            return

        try:
            with open(self.__file_path, mode="w") as fil:
                json.dump(self.__objects, fil)
        except (FileNotFoundError, PermissionError) as error:
            # print("Any Here")
            pass

    def new(self, obj: dict):
        """sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj["__class__"], obj["id"])
        self.__objects[key] = obj

    def all(self):
        """Returns the private objects holding all the data"""
        return self.__objects
