#!/usr/bin/python3
"""this module contains the tests for the User class """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """test case for the State class """

    def __init__(self, *args, **kwargs):
        """nitialisation of testing clas """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """check firstname """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """check last name """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """check email """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ check password"""
        new = self.value()
        self.assertEqual(type(new.password), str)
