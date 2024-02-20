#!/usr/bin/python3
'''Module defines Amenity'''

from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base, store
from sqlalchemy import Column, String


@store('place_amenities',
       name=(Column(String(128), nullable=False), ''),
       place_amenities=(relationship("Place",
                        secondary="place_amenity",
                        back_populates="amenities"),)
       )
class Amenity(BaseModel, Base):
    '''Amenity class.

    Atrrs:
        name: string
    '''
    __tablename__ = 'amenities'
