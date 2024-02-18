#!/usr/bin/python3
'''Module defines City'''

from models.base_model import BaseModel


class City(BaseModel):
    '''City class.

    Atrrs:
        state_id(str):
        name(str):
    '''
    state_id = ''
    name = ''

    def __init__(self, *args, **kwargs):
        '''Initiliaztion'''
        super().__init__(*args, **kwargs)
