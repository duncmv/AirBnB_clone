#!/user/bin/env python3
"""Module for testing the console"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage
import re
import os


class Helpers(unittest.TestCase):
    """Class to keep helper functions together"""

    @classmethod
    def setUpClass(cls):
        """This runs once before any of the tests"""
        try:
            os.rename("file.json", "tmp.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls):
        """This runs once after all of the tests are done"""
        try:
            os.unlink("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except IOError:
            pass

    def t_cmd_assert_false(self, cmd: str) -> str:
        """Run cmd and perform assert false on the output, return output
        Used to test if running a command is successful
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd))
            output = f.getvalue().strip()
        return output

    def t_cmd_assert_true(self, cmd: str) -> str:
        """Run cmd and perform assert true on the output, return output"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd(cmd))
            output = f.getvalue().strip()
        return output

    def t_fetch_model(self, model):
        """Fetches all the available instances of model"""
        objs = storage.all()
        if model:  # fetch only required
            return [str(v) for k, v in objs.items() if model in k]
        return [str(v) for v in objs.values()]  # Fetch all

    def t_trucate_store(self):
        """Remove the store file for recreation"""
        reg = r"\[(\w+)] \(([\w-]+)\)"
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"all")
            matches = re.findall(reg, f.getvalue().strip())
            for model, uuid in matches:
                HBNBCommand().onecmd("destroy {} {}".format(model, uuid))

    def t_create_model(self, modelname: str):
        """Creates a model and returns the UUID for testing"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {modelname}")
        return f.getvalue().strip()

    def t_destroy_model(self, name_id: str):
        """Destroys a model and returns the output for testing"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"destroy {name_id}")

        return f.getvalue().strip()

    def t_cmd_output_test(self, cmd: str, expected: str):
        """Test running a command and checking output against expected"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            output = f.getvalue().strip()
        self.assertIn(expected, output)

    def t_cmd_assert_equal(self, cmd: str, expected: str) -> str:
        """Run cmd and perform assert equal on the output, return output"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            output = f.getvalue().strip()
            self.assertEqual(output, expected)
        return output

    def t_cmd_output(self, cmd: str) -> str:
        """Runs a command and returns its output"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            output = f.getvalue().strip()
        return output


class TestHBNBCommand(Helpers):
    """The HBNHCommand tests class"""

    def test_empty_line(self):
        output = self.t_cmd_assert_false("")
        self.assertEqual(output, "")

    def test_prompt_string(self):
        """Test if the prompt string is in order"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_quit(self):
        """Test the quit command"""
        self.t_cmd_assert_true("quit")

    def test_EOF(self):
        """Test the EOF command"""
        self.t_cmd_assert_true("EOF")

    def test_cls(self):
        """Test the cls command"""
        self.t_cmd_assert_false("cls")
        uuid = self.t_create_model("User")
        output = self.t_cmd_output("all")
        self.assertTrue(output)  # True means the string is not empty
        output = self.t_cmd_assert_false("cls")
        self.assertFalse(output)  # The string is empty
        self.t_destroy_model(f"User {uuid}")  # Destroy the User

    def test_help(self):
        """Test the help"""
        txt = "Documented commands (type help <topic>):\n"
        txt += "========================================\n"
        self.t_cmd_output_test("help", txt)  # uses self.assertIn
        self.t_cmd_output_test("?", txt)  # uses self.assertIn
        self.t_cmd_assert_false("help all")
        self.t_cmd_assert_false("help EOF")
        self.t_cmd_assert_false("help count")
        self.t_cmd_assert_false("help create")
        self.t_cmd_assert_false("help destroy")
        self.t_cmd_assert_false("help help")
        self.t_cmd_assert_false("help quit")
        self.t_cmd_assert_false("help show")
        self.t_cmd_assert_false("help update")

    def test_create_command(self):
        """Tests for the create command"""
        self.t_cmd_output_test("create", "** class name missing **")
        self.t_cmd_output_test("create xyz", "** class doesn't exist **")
        # Create these models and test that creating is succeessful
        models = "BaseModel User City Place Amenity Review State".split(" ")
        uuids = [self.t_cmd_assert_false(f"create {mdl}") for mdl in models]

        # Test that each object can be retrieved
        for model, uuid in zip(models, uuids):
            self.t_cmd_output_test(f"show {model} {uuid}", uuid)

        # Test against the output of the all command
        output = self.t_cmd_output("all")
        for uuid in uuids:
            self.assertIn(uuid, output)
        # Test deleting all
        for model, uuid in zip(models, uuids):
            self.t_cmd_assert_false(f"destroy {model} {uuid}")

        # Test that deletion succeeded
        for model, uuid in zip(models, uuids):
            expected = "** no instance found **"
            self.t_cmd_output_test(f"show {model} {uuid}", expected)

    def test_update_command(self):
        """Tests update command"""
        self.t_cmd_output_test("update", "* class name missing **")
        self.t_cmd_output_test("update xyz", "** class doesn't exist **")
        self.t_cmd_output_test("update User", "** instance id missing **")

        ud = self.t_create_model("User")
        self.t_cmd_output_test(f"show User {ud}", ud)  # check that User exists
        self.t_cmd_output_test(f"update User {ud}", "attribute name missing")

        # Test for different ways of using the update command
        expected = """'email': 'abc@gmail.com'"""  # Update the nomal way
        self.t_cmd_output_test(f'update User {ud} email "abc@gmail.com"', "")
        self.t_cmd_output_test(f"show User {ud}", expected)  # Did it work?

        expected = """'age': 36"""  # Update using dot notation
        self.t_cmd_output_test(f'User.update("{ud}", "age", 36)', "")
        self.t_cmd_output_test(f"show User {ud}", expected)  # Did it work?

        expected = """'name': 'Michael'"""  # Update using dot notation
        self.t_cmd_output_test(
            f'User.update("{ud}", {{"name": "Michael"}})', "")
        self.t_cmd_output_test(f"show User {ud}", expected)  # Did it work?

        self.t_destroy_model(f"User {ud}")  # Destroy the  created user

    def test_show_command(self):
        """Tests for the show command"""
        self.t_cmd_output_test("show", "* class name missing **")
        self.t_cmd_output_test("show User", "** instance id missing **")
        self.t_cmd_output_test("show xyz", "** class doesn't exist **")

        uuid = self.t_create_model("User")
        self.t_cmd_output_test(f"show User {uuid}", uuid)
        self.t_cmd_output_test(f'User.show("{uuid}")', uuid)
        self.t_destroy_model(f"User {uuid}")

    def test_destroy_command(self):
        """Tests for the destroy command"""
        self.t_cmd_output_test("destroy", "** class name missing **")
        self.t_cmd_output_test("destroy User", "** instance id missing **")
        self.t_cmd_output_test("destroy xyz", "** class doesn't exist **")

        uuid = self.t_create_model("City")  # creating known model
        self.t_cmd_output_test(f"show City {uuid}", uuid)  # exists
        self.t_cmd_output_test(f"destroy City {uuid}", "")
        self.t_cmd_output_test(f"show City {uuid}", "** no instance found **")

        uuid = self.t_create_model("Place")  # creating known model
        self.t_cmd_output_test(f"show Place {uuid}", uuid)  # exists
        self.t_cmd_output_test(f'Place.destroy("{uuid}")', "")
        self.t_cmd_output_test(f"show Place {uuid}", "** no instance found **")

    def test_all_command(self):
        """Tests for the all command"""
        # Test if the all command returns a string bounded by '[' and ']'
        self.assertRegex(self.t_cmd_output("all"), r"(^\[.*]$)")

        # Create a user, place, city, and test they exists
        uuids, models = [], ("City", "User", "User", "User", "Place")
        for model in models:  # create them
            uuids.append(self.t_create_model(model))

        output = self.t_cmd_output("all")
        for uuid in uuids:  # test that the each uuid is present in the output
            self.assertIn(uuid, output)

        output = self.t_cmd_output("all User")
        for uuid in uuids[1:4]:  # test that all three users appear in output
            self.assertIn(uuid, output)

        output = self.t_cmd_output("User.all()")
        for uuid in uuids[1:4]:  # test that all three users appear in output
            self.assertIn(uuid, output)

        for model, uuid in zip(models, uuids):
            self.t_destroy_model(f"{model} {uuid}")  # destroy them

    def test_count_command(self):
        """Tests for the count command"""
        self.t_cmd_output_test("count", "* class name missing **")
        users = self.t_fetch_model("User")
        n_users = len(users)
        self.t_cmd_output_test("count User", "{}".format(n_users))
        self.t_cmd_output_test("count xyz", "** class doesn't exist **")

        uuids = [self.t_create_model("User") for _ in range(3)]
        self.t_cmd_output_test("count User", "{}".format(n_users+3))
        self.t_cmd_output_test("User.count()", "{}".format(n_users+3))

        for uuid in uuids:
            self.t_destroy_model(f"User {uuid}")


if __name__ == "__main__":
    unittest.main()
