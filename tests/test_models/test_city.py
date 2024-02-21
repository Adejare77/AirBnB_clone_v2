#!/usr/bin/python3
"""this module contains the tests for the City class """
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class test_City(test_basemodel):
    """ Test case for City class"""

    def __init__(self, *args, **kwargs):
        """ initialisation of testing class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """type checking state_id of city object"""
        new_city = self.value()
        
        self.assertEqual(type(new_city.state_id), str)

    def test_name(self):
        """ type checking name of city object"""
        new = self.value()
        self.assertEqual(type(new_city.name), str)
