#!/usr/bin/env python3
"""Models review test module"""
from models.review import Review
from models.base_model import BaseModel
import unittest


class TestReviewClass(unittest.TestCase):
    """test for class"""
    def test_is_subclass(self):
        """test for a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id(self):
        """thest for for attribute place_id for Review class"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        self.assertEqual(review.place_id, "")

    def test_user_id(self):
        """test for the user_id attr"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        self.assertEqual(review.user_id, "")

    def test_test(self):
        """test for the text attribute in the Review class"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        self.assertEqual(review.text, "")

    def test_to_dict_values(self):
        """test the values in dict"""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        review = Review()
        new_dict = review.to_dict()
        self.assertEqual(new_dict["__class__"], "Review")
        self.assertEqual(type(new_dict['created_at']), str)
        self.assertEqual(type(new_dict['updated_at']), str)
        self.assertEqual(new_dict['created_at'],
                         review.created_at.strftime(time))
        self.assertEqual(new_dict['updated_at'],
                         review.updated_at.strftime(time))

    def test_str(self):
        """test for output str method"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
