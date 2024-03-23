#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    # This enforces a character encoding latin1 on the columns
    __table_args__ = {
        'mysql_charset': 'latin1'
    }
    name = Column(String(128), nullable=False)
    # This is for DBStorage
    cities = relationship("City", cascade="all, delete, delete-orphan",
                          backref="state")

    # This is for FileStorage
    @property
    def cities(self) -> list:
        """returns list of City instances with state_id
        equals to the current State.id. It will be the
        FileStorage relationship between State and City
        """
        from models import storage
        all_objs = storage.all()
        list_cities = []
        for k, v in all_objs.items():
            """ since State.id is the primary key to City.state_id
            Recall, v is an instance and not a dictionary, thus,
            v.__dict__['...']"""
            if (k.split(".")[0] == "City" and self.id ==
               v.__dict__['state_id']):
                list_cities.append(v)
        return list_cities
