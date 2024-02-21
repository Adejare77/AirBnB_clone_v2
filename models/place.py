#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey("places.id"),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        reviews = relationship("Review", cascade="all, delete, delete-orphan",
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """returns list of Review instances with place_id equals
            to the current Place.id"""
            from models import storage

            all_objs = storage._FileStorage__objects
            list_places = []
            for k, v in all_objs.items():
                # since Place.id is the primary key to place_id
                if (k.split(".")[0] == "Review" and self.id == v['place_id']):
                    list_places.append(v)
            return list_places

        @property
        def amenities(self):
            """list of Amenity instances based on the attribute
            amenity_ids that contians all Amenity.id linked to the
            place"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """handles append method for adding an Amenity.id
            to the attribute amenity_ids"""
            if (type(obj).__name__ == 'Amenity' and
               obj.id is not self.amenity_ids):
                self.amenity_ids.append(obj.id)
