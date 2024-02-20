#!/usr/bin/python3
'''Module defines Place'''

from models.base_model import BaseModel, Base, store
from models.review import Review
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import List


@store('reviews',
        city_id=(Column(String(60), ForeignKey('cities.id'),
                        nullable=False), ''),
        user_id=(Column(String(60), ForeignKey('users.id'),
                        nullable=False), ''),
        name=(Column(String(128), nullable=True), ''),
        description=(Column(String(1024)), ''),
        number_rooms=(Column(Integer, nullable=False, default=0), 0),
        number_bathrooms=(Column(Integer, nullable=False, default=0), 0),
        max_guest=(Column(Integer, nullable=False, default=0), 0),
        price_by_night=(Column(Integer, nullable=False, default=0), 0),
        latitude=(Column(Float), 0.0),
        longitude=(Column(Float), 0.0),
        reviews=(relationship('Review', backref='place',
                              cascade='all, delete-orphan'), ),
        amenity_ids=([], [])
      )
class Place(BaseModel, Base):
    '''Place class.

    Atrrs:
        __tablename__: name of mapped table
        city_id(str)
        user_id(str)
        name(str):
        description(str)
        number_rooms(int)
        number_bathrooms(int)
        max_guest(int)
        price_by_night(int):
        latitude(float):
        longitude(float): initilaized to 0.0
        amenity_ids(list:str): it will be list of Amenity.id
    '''
    __tablename__ = 'places'

    @property
    def reviews(self) -> List:
        """cities getter attribute"""
        from models import storage
        return [v for v in storage.all(Review).values()
                if v.place_id == self.id]
