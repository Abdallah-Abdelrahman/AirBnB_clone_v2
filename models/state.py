#!/usr/bin/python3
'''Module defines State'''

from models.base_model import BaseModel, Base, store
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from typing import List


@store('cities',
       name=(Column(String(128), nullable=False), ''),
       cities=(relationship('City', cascade='all, delete-orphan',
                            backref='state'), )
       )
class State(BaseModel, Base):
    '''State class

    Atrrs:
        name(str):
    '''
    __tablename__ = "states"

    @property
    def cities(self) -> List:
        """cities getter attribute"""
        from models import storage
        return [v for v in storage.all(City).values() if v.state_id == self.id]
