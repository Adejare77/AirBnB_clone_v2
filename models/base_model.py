#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model
        Args:
            args: Won't be used
            kwargs(dict): contains key, value of an instance
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            if kwargs.get('created_at'):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if kwargs.get('updated_at'):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if kwargs.get('__class__'):
                del kwargs['__class__']

            if not kwargs.get('id'):
                self.id = str(uuid.uuid4())
            if not kwargs.get('created_at'):
                self.created_at = datetime.now()
            if not kwargs.get('updated_at'):
                self.updated_at = datetime.now()

            self.__dict__.update(**kwargs)
        self.save()

    def __str__(self):
        """Returns a string representation of the instance"""
        """
        Since, every instance inherits from Base=declarative_base(), then by
        default, they'll inherits "_sa_instance_state" into their dictionary.
        But, I don't want this _sa_instance_state to be printed, thus
        the purpose of making a copy
        """
        dict_copy = self.__dict__.copy()
        if hasattr(self, "_sa_instance_state"):
            del dict_copy['_sa_instance_state']
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, dict_copy)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if dictionary.get('_sa_instance_state'):
            del dictionary['_sa_instance_state']
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Delete current instance from the storage"""
        from models import storage
        storage.delete(self)
