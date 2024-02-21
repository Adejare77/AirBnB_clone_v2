#!/usr/bin/python3
""" Test module for the console"""
import unittest
from models.base_model import BaseModel
from models.user import User
import models
import sys
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
import uuid
import json
import sqlalchemy
from os import remove
import os 


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "test of filestorage")
class TestCreate(unittest.TestCase):
    """ tests `do_create()` with file storage
    Usage:
        create <classname>
    """
    @classmethod
    def setUpClass(self):
        self.console1 = HBNBCommand()

    @classmethod
    def tearDownClass(self):
        del self.console1

    def test_create_missing_class(self):
        """test create with a missing class"""
        expected = "** class name missing **"

        with patch("sys.stdout", new=StringIO()) as output:
            input_line = "create"
            self.console1.onecmd(input_line)
            self.assertEqual(expected, output.getvalue().strip())

    def test_create_wrong_class(self):
        """tests create with wrong class"""
        expected = "** class doesn't exist **"

        with patch("sys.stdout", new=StringIO()) as output:
            input_line = "create jog"
            self.console1.onecmd(input_line)
            self.assertEqual(expected, output.getvalue().strip())

    def test_create_succesful(self):
        """tests successful create command"""

        with patch("sys.stdout", new=StringIO()) as output:
            input_line = "create User"
            self.console1.onecmd(input_line)
            id_string = output.getvalue().strip()
            user_id = uuid.UUID(output.getvalue().strip())
            self.assertEqual(type(user_id), uuid.UUID)
            self.assertIn("User." + id_string, models.storage.all().keys())


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "test of database storage")
class TestCreateDB(unittest.TestCase):
    """ Testing the create command(db)
    Usage:
        create <classname>
    """

    @classmethod
    def setUpClass(self):
        self.console1 = HBNBCommand()

    @classmethod
    def tearDownClass(self):
        del self.console1

    def test_create_class_successful(self):
        """ test to check for successfull class creation"""
        with patch("sys.stdout", new=StringIO()) as output:
            # use mysqldb to :
            # create connection and cursor
            test_conn = MySQLdb.connect(host=os.getenv('HBNB__MYSQL_HOST'),
                                        user=os.getenv('HBNB_MYSQL_USER'),
                                        passwd=os.getenv('HBNB_MYSQL_PWD'),
                                        port=3306, db=os.getenv('HBNB_MYSQL_DB'))
            cur = test_conn.cursor()
            
            # get current number of record in test table
            # excecute console command
            self.console1.onecmd(input_line) ud
            input_line = "create City name=Detroit"
            # get new number of records and assert that the diff is +1            
            id_string = output.getvalue().strip()
            self.assertIn("")

