#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    name = Column("name", String(128), nullable=False)

    cities = relationship("City", back_populates="state",
                          cascade="all, delete-orphan")

    @property
    def cities(self):
        city_list = []
        all_cities = storage.all(City).values()
        for city in all_cities:
            if self.id == city.state_id:
                city_list.append(city)
        return city_list
