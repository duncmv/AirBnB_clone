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
        """Run cmd and perform assert false on the output, return output"""
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

    def t_cmd_assert_equal(self, cmd: str, expected: str) -> str:
        """Run cmd and perform assert equal on the output, return output"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            output = f.getvalue().strip()
            self.assertEqual(output, expected)
        return output

    def t_fetch_model(self, model):
        """Fetches all the available instances of model"""
        objs = storage.all()
        return [str(v) for k, v in objs.items() if model in k]

    def t_create_model(self, modelname: str):
        """Creates a model and returns the UUID for testing"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {modelname}")
            output = f.getvalue().strip()
        return output

    def t_destroy_model(self, name_id: str):
        """Destroys a model and returns the output for testing"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(f"destroy {name_id}")
            output = f.getvalue().strip()

        return output

    def t_cmd_output_test(self, cmd: str, expected: str):
        """Test running a command and checking output against expected"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        self.assertIn(expected, f.getvalue().strip())

    def t_cmd_output(self, cmd: str) -> str:
        """Runs a command and returns its output"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            ouput = f.getvalue().strip()
        return ouput


class TestHBNBCommand(Helpers):
    """The HBNHCommand tests class"""

    def test_show_command(self):
        """Tests for the show command"""
        self.t_cmd_output_test("show", "* class name missing **")
        self.t_cmd_output_test("show User", "** instance id missing **")
        self.t_cmd_output_test("show xyz", "** class doesn't exist **")

        uuid = self.t_create_model("User")
        self.t_cmd_output_test(f"show User {uuid}", uuid)
        self.t_cmd_output_test(f'User.show("{uuid}")', uuid)
        self.t_destroy_model(f"User {uuid}")

    def test_create_command(self):
        """Tests for the create command"""
        self.t_cmd_output_test("create", "** class name missing **")
        self.t_cmd_output_test("create xyz", "** class doesn't exist **")

        uuid = self.t_create_model("City")  # creating known model
        self.t_cmd_output_test(f"show City {uuid}", uuid)
        self.t_destroy_model(f"City {uuid}")

    def test_destroy_command(self):
        """Tests for the destroy command"""
        self.t_cmd_output_test("destroy", "** class name missing **")
        self.t_cmd_output_test("destroy User", "** instance id missing **")
        self.t_cmd_output_test("destroy xyz", "** class doesn't exist **")

        uuid = self.t_create_model("City")  # creating known model
        self.t_cmd_output_test(f"show City {uuid}", uuid)  # exists
        self.t_cmd_output_test(f"destroy City {uuid}", "")  # destroy it
        self.t_cmd_output_test(f"show City {uuid}", "** no instance found **")

        uuid = self.t_create_model("Place")  # creating known model
        self.t_cmd_output_test(f"show Place {uuid}", uuid)  # exists
        self.t_cmd_output_test(f'Place.destroy("{uuid}")', "")  # destroy it
        self.t_cmd_output_test(f"show Place {uuid}", "** no instance found **")

    def test_all_command(self):
        """Tests for the all command"""
        # Test the all command: output is bounded by '[' and ']'
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
        self.t_cmd_output_test("count xyz", "** class doesn't exist **")

        self.t_create_model("BaseModel")
        self.t_cmd_assert_equal("count BaseModel", "1")
        self.t_create_model("User")
        self.t_cmd_assert_equal("count User", "1")
        self.t_create_model("State")
        self.t_cmd_assert_equal("count State", "1")
        self.t_create_model("Place")
        self.t_cmd_assert_equal("count Place", "1")
        self.t_create_model("City")
        self.t_cmd_assert_equal("count City", "1")
        self.t_create_model("Amenity")
        self.t_cmd_assert_equal("count Amenity", "1")
        self.t_create_model("Review")
        self.t_cmd_assert_equal("count Review", "1")


class TestHBNBCommand_update(Helpers):

    def test_update_missing_class(self):

        self.t_cmd_assert_equal("update", "** class name missing **")
        self.t_cmd_assert_equal(".update()", "** class name missing **")

    def test_update_invalid_class(self):
        self.t_cmd_assert_equal("update MyModel", "** class doesn't exist **")
        self.t_cmd_output_test("MyModel.update()", "** class doesn't exist **")

    def test_update_missing_id_space_notation(self):
        output = self.t_cmd_assert_false("update BaseModel")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("update User")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("update State")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("update City")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("update Amenity")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("update Place")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("update Review")
        self.assertEqual("** instance id missing **", output)

    def test_update_missing_id_dot_notation(self):
        output = self.t_cmd_assert_false("BaseModel.update()")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("User.update()")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("State.update()")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("City.update()")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("Amenity.update()")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("Place.update()")
        self.assertEqual("** instance id missing **", output)
        output = self.t_cmd_assert_false("Review.update()")
        self.assertEqual("** instance id missing **", output)

    def test_update_invalid_id_space_notation(self):
        output = self.t_cmd_assert_false("update BaseModel 1")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("update User 1")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("update State 1")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("update City 1")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("update Amenity 1")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("update Place 1")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("update Review 1")
        self.assertEqual("** no instance found **", output)

    def test_update_invalid_id_dot_notation(self):
        output = self.t_cmd_assert_false("BaseModel.update(1)")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("User.update(1)")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("State.update(1)")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("City.update(1)")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("Amenity.update(1)")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("Place.update(1)")
        self.assertEqual("** no instance found **", output)
        output = self.t_cmd_assert_false("Review.update(1)")
        self.assertEqual("** no instance found **", output)

    def test_update_missing_attr_name_space_notation(self):
        output = self.t_cmd_assert_false("create BaseModel")
        output = self.t_cmd_assert_false("update BaseModel {}".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create User")
        output = self.t_cmd_assert_false("update User {}".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create State")
        output = self.t_cmd_assert_false("update State {}".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create City")
        output = self.t_cmd_assert_false("update City {}".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create Amenity")

        output = self.t_cmd_assert_false("update Amenity {}".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create Place")
        output = self.t_cmd_assert_false("update Place {}".format(output))
        self.assertEqual("** attribute name missing **", output)

    def test_update_missing_attr_name_dot_notation(self):
        output = self.t_cmd_assert_false("create BaseModel")
        output = self.t_cmd_assert_false("BaseModel.update({})".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create User")
        output = self.t_cmd_assert_false("User.update({})".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create State")
        output = self.t_cmd_assert_false("State.update({})".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create City")
        output = self.t_cmd_assert_false("City.update({})".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create Amenity")
        output = self.t_cmd_assert_false("Amenity.update({})".format(output))
        self.assertEqual("** attribute name missing **", output)

        output = self.t_cmd_assert_false("create Place")
        output = self.t_cmd_assert_false("Place.update({})".format(output))
        self.assertEqual("** attribute name missing **", output)

    def test_update_missing_attr_value_space_notation(self):
        output = self.t_create_model("BaseModel")
        output = self.assertFalse(f"update BaseModel {output} attr_name")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("User")
        self.t_cmd_assert_false("update User {} attr_name".format(output))
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("State")
        self.t_cmd_assert_false("update State {} attr_name".format(output))
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("City")
        self.t_cmd_assert_false("update City {} attr_name".format(output))
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("Amenity")
        self.t_cmd_assert_false("update Amenity {} attr_name".format(output))
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("Place")
        self.t_cmd_assert_false("update Place {} attr_name".format(output))
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("Review")
        self.t_cmd_assert_false("update Review {} attr_name".format(output))
        self.assertEqual("** value missing **", output)

    def test_update_missing_attr_value_dot_notation(self):
        output = self.t_create_model("BaseModel")
        output = self.t_cmd_assert_false(
            f"BaseModel.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("User")
        output = self.t_cmd_assert_false(f"User.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("State")
        output = self.t_cmd_assert_false(f"State.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("City")
        output = self.t_cmd_assert_false(f"City.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("Amenity")
        output = self.t_cmd_assert_false(
            f"Amenity.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("Place")
        output = self.t_cmd_assert_false(f"Place.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

        output = self.t_create_model("Review")
        output = self.t_cmd_assert_false(f"Review.update({output}, attr_name)")
        self.assertEqual("** value missing **", output)

    def test_update_valid_string_attr_space_notation(self):

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        testCmd = "update User {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        testCmd = "update State {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "update City {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        testCmd = "update Review {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tId = output.getvalue().strip()
        testCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tId = output.getvalue().strip()
        testCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tId = output.getvalue().strip()
        testCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tId = output.getvalue().strip()
        testCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        testCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tId = output.getvalue().strip()
        testCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tId = output.getvalue().strip()
        testCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} max_guest 98".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        testCmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} latitude 7.2".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        testCmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "update BaseModel {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        testCmd = "update User {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        testCmd = "update State {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "update City {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        testCmd = "update Amenity {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        testCmd = "update Review {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "BaseModel.update({}".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        testCmd = "User.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        testCmd = "State.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "City.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        testCmd = "Amenity.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        testCmd = "Review.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


if __name__ == "__main__":
    unittest.main()
