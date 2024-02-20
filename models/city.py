#!/usr/bin/python3
'''Module defines City'''

from models.base_model import BaseModel, Base, store
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


@store('places',
       name=(Column(String(128), nullable=False), ''),
       state_id=(Column(String(60), ForeignKey('states.id'),
                        nullable=False), ''),
       places=(relationship('Place', backref='cities',
                            cascade='all, delete-orphan'), )
       )
class City(BaseModel, Base):
    '''City class.

    Atrrs:
        state_id(str):
        name(str):
    '''
    __tablename__ = 'cities'
