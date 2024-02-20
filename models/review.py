#!/usr/bin/python3
'''Module defines Review'''

from models.base_model import BaseModel, Base, store
from sqlalchemy import Column, String, ForeignKey


@store(
        text=(Column(String(1024), nullable=False), ''),
        place_id=(Column(String(60), ForeignKey('places.id'),
                         nullable=False), ''),
        user_id=(Column(String(60), ForeignKey('users.id'),
                        nullable=False), '')
       )
class Review(BaseModel, Base):
    '''Review class.

    Atrrs:
        __tablename__: name of maped table
        place_id(str):
        user_id(str):
        text(str):
    '''
    __tablename__ = 'reviews'
