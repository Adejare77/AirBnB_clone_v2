#!/usr/bin/python3
"""Using Database as a Storage Engine for hbnb clone"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from os import getenv

class DBStorage:
    """Alternate storage to FileStorage"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')),pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class"""
        objects = {}
        if cls:
            # Returns a SQL statement into data which contains all rows data
            data = self.__session.query(cls)
            for sql_stment in data:
                key = type(sql_stment).__name__  + "." + sql_stment.id
                objects.update({key: sql_stment})
        else:
            _classes = [Amenity, City, Place, Review, State, User]
            for _cls in _classes:
                # Returns a SQL statement into data
                data = self.__session.query(_cls)
                for sql_stment in data:
                    key = type(sql_stment).__name__  + "." + sql_stment.id
                    objects.update({key: sql_stment})
        return objects


    def new(self, obj):
        """add the obj to the current database session (self.__session)"""
        # We don't need to query, since we aren't interested in getting any data
        # but to add
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)
        # Base.metadata.tables[]

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)"""
        # create all tables from the engine
        Base.metadata.create_all(self.__engine)
        # expired_on_commit=False disables automatic refresh of DB on commit
        Session = sessionmaker(self.__engine, expire_on_commit=False)
        # ensures  each thread has its own unique session object,
        # preventing conflicts and ensuring thread safety
        self.__session = scoped_session(Session)()
