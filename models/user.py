#!/usr/bin/python3
'''Module defines `User` class'''

from models.base_model import BaseModel, Base, store
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


@store('reviews', 'places',
       email=(Column(String(128), nullable=False), ''),
       password=(Column(String(128), nullable=False), ''),
       first_name=(Column(String(128)), ''),
       last_name=(Column(String(128)), ''),
       reviews=(relationship('Review', backref='user',
                             cascade='all, delete-orphan'), ),
       places=(relationship('Place', backref='user',
                            cascade='all, delete-orphan'), )
       )
class User(BaseModel, Base):
    '''User class.

    Atrrs:
        email(str):
        password(str):
        first_name(str):
        last_name(str):
    '''
    __tablename__ = 'users'
