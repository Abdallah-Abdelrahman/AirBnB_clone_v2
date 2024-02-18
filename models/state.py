#!/usr/bin/python3
'''Module defines State'''

from models.base_model import BaseModel


class State(BaseModel):
    '''State class

    Atrrs:
        name(str):
    '''
    name = ''

    def __init__(self, *args, **kwargs):
        '''Initiliaztion'''
        super().__init__(*args, **kwargs)
