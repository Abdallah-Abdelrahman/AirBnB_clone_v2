#!/usr/bin/python3
'''Module creates a unique FileStorage instance for the application

Attrs:
    storage: an instance of FileStorage
'''

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv


db = (False, True)['db' == getenv("HBNB_TYPE_STORAGE")]

if db:
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
