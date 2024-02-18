#!/usr/bin/python3
'''Module defines Place'''

from models.base_model import BaseModel


class Place(BaseModel):
    '''Place class.

    Atrrs:
        city_id(str)
        user_id(str)
        name(str):
        description(str)
        number_rooms(int)
        number_bathrooms(int)
        max_guest(int)
        price_by_night(int):
        latitude(float):
        longitude(float): initilaized to 0.0
        amenity_ids(list:str): it will be list of Amenity.id
    '''
    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        '''Initiliaztion'''
        super().__init__(*args, **kwargs)
