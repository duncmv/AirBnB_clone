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

    def t_create_unknown_model(self):
        """Test creating an unknown model"""
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("create UnknownModel")
        output = self.stdout_.getvalue().strip()
        self.assertIn("Class doesn't exist", output)

    def t_create_known_model(self, modelname):
        """Test creating a known model"""
        with patch("sys.stdout", new=self.stdout_):  # Issues a known command
            self.hbnb.onecmd(f"create {modelname}")

        output = self.stdout_.getvalue().strip()
        self.assertEqual(output.count("-"), 4)  # it has 4 hyphens
        self.assertEqual(len(output.split("-")), 5)  # string has 5 parts


class TestHBNBCommand(Helpers):
    """The HBNHCommand tests class"""

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

    def test_show_command(self):
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("show")
        self.assertIn("class name missing",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("show UnknownModel")
        self.assertIn("class doesn't exist",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("show User")
        self.assertIn("instance id missing",
                      self.stdout_.getvalue().strip())

        # Add more test cases for show command

    def test_destroy_command(self):
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("destroy")
        self.assertIn("class name missing",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("destroy UnknownModel")
        self.assertIn("class doesn't exist",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("destroy User")
        self.assertIn("instance id missing",
                      self.stdout_.getvalue().strip())

        # Add more test cases for destroy command

    def test_all_command(self):
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("all UnknownModel")
        self.assertIn("class doesn't exist",
                      self.stdout_.getvalue().strip())

        # Add more test cases for all command

    def test_update_command(self):
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("update")
        self.assertIn("class name missing",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("update UnknownModel")
        self.assertIn("class doesn't exist",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("update User")
        self.assertIn("instance id missing",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("update User bef0b8")
        self.assertIn("attribute name missing",
                      self.stdout_.getvalue().strip())

        # Add more test cases for update command

    def test_count_command(self):
        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("count")
        self.assertIn("class name missing",
                      self.stdout_.getvalue().strip())

        with patch("sys.stdout", new=self.stdout_):
            self.hbnb.onecmd("count UnknownModel")
        self.assertIn("class doesn't exist",
                      self.stdout_.getvalue().strip())

        # Add more test cases for count command

    def test_quit_command(self):
        with self.assertRaises(SystemExit):
            self.hbnb.onecmd("quit")

    def test_EOF_command(self):
        with self.assertRaises(SystemExit):
            self.hbnb.onecmd("EOF")

    def test_cls_command(self):
        with patch("os.system") as mock_system:
            self.hbnb.onecmd("cls")
            mock_system.assert_called_once_with("cls")

    # Add more tests as needed


if __name__ == "__main__":
    unittest.main()
