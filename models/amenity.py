#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """agreeable conditions for sustenance"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    # I commented below because I've backref it from place.py
    # place_amenities = relationship("Place", secondary=place_amenity)
    # __table_args__ = {
    #     'mysql_charset': 'latin1'
    # }
