#!/usr/bin/python3
'''Module defines BaseModel class'''

from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel:
    '''BaseModel class'''
    def __init__(self, *args, **kwargs):
        '''Instantiate an instance'''
        self.id = str(uuid4())
        if not len(kwargs):
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
            return
        for k, v in kwargs.items():
            if k != '__class__':
                # TODO: if *_at is not valid date string
                setattr(self, k, v if k not in ('updated_at', 'created_at')
                        else datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f'))

    def save(self):
        '''updates the public instance attribute updated_at'''
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        '''returns a dictionary containing all keys/values of __dict__

        Return:
            __dict__ plus __class__ represents class name
        '''
        _dict = {k: v.isoformat() if isinstance(v, datetime) else
                 v for k, v in self.__dict__.items()}
        _dict['__class__'] = self.__class__.__name__
        return _dict

    def __str__(self):
        '''Instance representaion'''
        return '[{}] ({}) {}'.format(self.__class__.__name__,
                                     self.id, self.__dict__)
