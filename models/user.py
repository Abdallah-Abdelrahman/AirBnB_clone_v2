#!/usr/bin/python3
'''Module defines `User` class'''

from models.base_model import BaseModel


class User(BaseModel):
    '''User class.

    Atrrs:
        email(str):
        password(str):
        first_name(str):
        last_name(str):
    '''
    email = ''
    password = ''
    first_name = ''
    last_name = ''

    def __init__(self, *args, **kwargs):
        '''Initiliaztion'''
        super().__init__(*args, **kwargs)
