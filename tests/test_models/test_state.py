#!/usr/bin/python3
"""This module contains test cases for"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """ test case for the State class"""

    def __init__(self, *args, **kwargs):
        """ initialisation of testing class"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ type checking the state name attribute"""
        new_state_obj = self.value()
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertNone(new_state_obj)
        else:
            self.assertEqual(type(new_state_obj.name), str)
