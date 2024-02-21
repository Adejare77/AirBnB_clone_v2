#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    # This is for DBStorage
    cities = relationship("City", cascade="all, delete, delete-orphan",
                          backref="state")
    # This is for FileStorage

    @property
    def cities(self):
        """returns list of City instances with state_id
        equals to the current State.id. It will be the
        FileStorage relationship between State and City
        """
        from models import storage
        all_objs = storage.all()
        list_cities = []
        for k, v in all_objs.items():
            # since State.id is the primary key to City.state_id
            if (k.split(".")[0] == "City" and self.id == v['state_id']):
                list_cities.append(v)
        return list_cities
