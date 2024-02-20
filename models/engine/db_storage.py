#!/usr/bin/python3
""" 
This module defines a class to manage Database Storage for the airbnb clone
"""
import os
from ..models.base_model import BaseModel, Base
from ..models.state import State
from ..models.city import City
from ..models.user import User
from ..models.amenity import Amenity
from ..models.place import Place
from ..models.review import Review
from sqlalchemy import create_engine

user = os.getenv(HBNB_MYSQL_USER)
passwd = os.getenv(HBNB_MYSQL_PWD)
host = os.getenv(HBNB_MYSQL_HOST)
db = os.getenv(HBNB_MYSQL_DB) 


class DBStorage:
    """ file defintion for DBStorage """

    __engine = None
    __session = None

    def __init__(self):
        """ instantiation for Storage"""
        self.__engine = create_engine("""mysql+mysqldb://{}:{}@{}/{}""".format(
                                      user, passwd,host,db))

        if user == "test":
            Base.metadata.drop_all(bind=self.__engine) 

        Base.metadata.create_all(bind=self.__engine) 

    def all(self, cls=None):
        """query on the database session"""

        if cls is None:
            query_results  = self.__session.query(State, City, Amenity, Place, Review).all()
        else:
            query_results  = self.__session.query(cls).all()

        #how results will be displayed
        #create and populate dictionary
        dictionary = {}
        for row in query_results:
            d_key = cls+"."+row.id
            dictionary[d.key] = row
        return dictionary

    def new(self):
        """add object to database"""
        self.__session.add()

    def save(self):
        """commit changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes existing objects from the database"""
        if obj != None:
            self.__session.delete(obj)

    def reload(self):
        """ creates all tables in the database"""
        Base.metadata.create_all(bind=self.__engine) 
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        
    
    
