#!/user/bin/env python3
"""Module for testing the console"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class Helpers(unittest.TestCase):
    """Class to keep helper functions together"""

    def setUp(self):
        """Test startup settings happen here"""
        self.hbnb = HBNBCommand()
        self.stdout_ = StringIO()

    def tearDown(self):
        """Test final cleanups happen here"""
        self.stdout_.close()

    def clear_stdout(self):
        """Clears the stdout buffer"""
        self.stdout_.truncate(0)
        self.stdout_.seek(0)

    def t_create_unknown_model(self):
        """Test creating an unknown model"""
        self.clear_stdout()
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("create UnknownModel")
        output = self.stdout_.getvalue().strip()
        self.assertIn("Class doesn't exist", output)
        self.stdout_.truncate()

    def t_create_known_model(self, modelname: str):
        """Test creating a known model"""
        self.clear_stdout()
        with patch("sys.stdout", new=self.stdout_):  # Issues a known command
            self.hbnb.onecmd(f"create {modelname}")

        output = self.stdout_.getvalue().strip()
        self.assertEqual(output.count("-"), 4)  # it has 4 hyphens
        self.assertEqual(len(output.split("-")), 5)  # string has 5 parts
        return output

    def t_cmd_output_test(self, cmd: str, expected: str):
        """Test running a command and checking output against expected"""
        self.clear_stdout()
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd(cmd)
        self.assertIn(expected, self.stdout_.getvalue().strip())


class TestHBNBCommand(Helpers):
    """The HBNHCommand tests class"""

    def test_show_command(self):
        """Tests for the show command"""
        self.t_cmd_output_test("show", "* class name missing **")
        self.t_cmd_output_test("show Unknown", "** class doesn't exist **")
        self.t_cmd_output_test("show User", "** instance id missing **")

        uuid = self.t_create_known_model("User")
        self.t_cmd_output_test(f"show User {uuid}", uuid)

    def test_create_command(self):
        """Tests for the create command"""
        self.t_create_known_model("BaseModel")  # creating an unknown model

        self.t_create_known_model("User")  # creating known model
        self.t_create_known_model("Amenity")  # creating known model
        self.t_create_known_model("State")  # creating known model
        self.t_create_known_model("City")  # creating known model
        self.t_create_known_model("Place")  # creating known model
        self.t_create_known_model("Review")  # creating known model
        self.t_create_known_model("BaseModel")  # creating known model


if __name__ == "__main__":
    unittest.main()
