#!/usr/bin/python3
'''This Module defines file storage class'''

from json import loads, dumps


class FileStorage:
    ''' FileStorage class.

    Attrs:
        __file_path(str): path to the JSON file
        __objects(dictionary): empty but will store all objects
            by <class name>.id
    '''

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        '''Returns the dictionary `__objects`'''
        return FileStorage.__objects

    def new(self, obj):
        '''Sets in __objects the obj with key <obj class name>.id'''
        if not obj:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        '''Serializes __objects to the JSON file'''

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            file.write(dumps(FileStorage.__objects,
                             default=lambda obj: obj.to_dict()))

    def reload(self):
        '''Deserializes the JSON file to __objects'''
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                from models.base_model import BaseModel
                from models.user import User
                from models.amenity import Amenity
                from models.city import City
                from models.place import Place
                from models.review import Review
                from models.state import State

                cls = {
                        'BaseModel': BaseModel, 'User': User,
                        'Amenity': Amenity, 'City': City,
                        'Place': Place, 'Review': Review,
                        'State': State
                      }
                for k, v in loads(file.read()).items():
                    FileStorage.__objects[k] = cls[v['__class__']](**v)
        except Exception:
            pass
