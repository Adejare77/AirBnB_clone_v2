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
import MySQLdb
from models.city import City
from models.base_model import BaseModel

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
                 "skipped test is for database storage")
class TestCreateDB(unittest.TestCase):
    """ Testing the create command(db)
    Usage:
        create <classname>
    """

    @classmethod
    def setUpClass(self):
        self.console1 = HBNBCommand()
        #call setup function , to populate table
        
        setup_conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                                user=os.getenv('HBNB_MYSQL_USER'),
                                                passwd=os.getenv('HBNB_MYSQL_PWD'),
                                                port=3306, db=os.getenv('HBNB_MYSQL_DB'))
        cur = setup_conn.cursor()
        cur.execute(f"INSERT INTO cities (id, state_id, name) VALUES (1, 1, 'San Francisco'), (2, 1, 'San Jose'), (3, 1, 'Los Angeles'), (4, 1, 'Fremont'), (5, 1, 'Livermore');")
        # cur.execute(f"INSERT INTO cities (id, state_id, name) VALUES (1, 'San Francisco'), (1, 'San Jose'), (1, 'Los Angeles'), (1, 'Fremont'), (1, 'Livermore');")
        # cur.execute(f"INSERT INTO cities (id, state_id, name) VALUES (2, 'Page'), (2, 'Phoenix');")
        # cur.execute(f"INSERT INTO cities (id, state_id, name) VALUES (3, 'Dallas'), (3, 'Houston'), (3, 'Austin');")
        # cur.execute(f"INSERT INTO cities (id, state_id, name) VALUES (4, 'New York');")
        # cur.execute(f"INSERT INTO cities (id, state_id, name) VALUES (5, 'Las Vegas'), (5, 'Reno'), (5, 'Henderson'), (5, 'Carson City');")

        setup_conn.commit()
        cur.close()
        setup_conn.close()
        
    @classmethod
    def tearDownClass(self):
        setup_conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                                user=os.getenv('HBNB_MYSQL_USER'),
                                                passwd=os.getenv('HBNB_MYSQL_PWD'),
                                                port=3306, db=os.getenv('HBNB_MYSQL_DB'))
        cur = setup_conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS cities")

        cur.close()
        setup_conn.close()
        del self.console1

    def test_create_class_successful(self):
        """ test to check for successfull class creation"""
        with patch("sys.stdout", new=StringIO()) as output:
            # use mysqldb to :
            # create connection and cursor
            test_conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                        user=os.getenv('HBNB_MYSQL_USER'),
                                        passwd=os.getenv('HBNB_MYSQL_PWD'),
                                        port=3306, db=os.getenv('HBNB_MYSQL_DB'))
            cur = test_conn.cursor()

            # get current number of record in test table
            num_rows = cur.rowcount
            # excecute console command
            input_line = "create City name=Detroit"
            self.console1.onecmd(input_line) 
            # get new number of records and assert that the diff is +1 
            num_rows2 = cur.rowcount
            self.assertEqual((num_rows2 - num_rows), 1)           
            # id_string = output.getvalue().strip()
            # self.assertIn("")

