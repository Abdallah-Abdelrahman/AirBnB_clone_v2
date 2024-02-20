#!/usr/bin/python3
'''Module defines City'''

from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey

from os import getenv

db = (False, True)['db' == getenv("HBNB_TYPE_STORAGE")]


class City(BaseModel, Base):
    '''City class.

    Atrrs:
        state_id(str):
        name(str):
    '''
    __tablename__ = 'cities'
    if db:
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
    else:
        state_id = ''
        name = ''
