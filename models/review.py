#!/usr/bin/python3
'''Module defines Review'''

from models.base_model import BaseModel


class Review(BaseModel):
    '''Review class.

    Atrrs:
        place_id(str):
        user_id(str):
        text(str):
    '''
    place_id = ''
    user_id = ''
    text = ''

    def __init__(self, *args, **kwargs):
        '''Initiliaztion'''
        super().__init__(*args, **kwargs)
