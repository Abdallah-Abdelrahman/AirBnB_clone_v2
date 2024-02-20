#!/usr/bin/python3
'''Module defines `User` class'''

from models.base_model import BaseModel, Base, store
from sqlalchemy import Column, String


@store(email=Column(String(128), nullable=False),
       password=Column(String(128)),
       first_name=Column(String(128)), last_name=Column(String(128)))
class User(BaseModel, Base):
    '''User class.

    Atrrs:
        email(str):
        password(str):
        first_name(str):
        last_name(str):
    '''
    __tablename__ = 'users'
