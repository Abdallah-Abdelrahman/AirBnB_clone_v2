#!/usr/bin/python3
'''Module defines Amenity'''

from models.base_model import BaseModel


class Amenity(BaseModel):
    '''Amenity class.

    Atrrs:
        name: string
    '''
    name = ''

    def __init__(self, *args, **kwargs):
        '''Initiliaztion'''
        super().__init__(*args, **kwargs)
