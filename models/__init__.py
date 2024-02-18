#!/usr/bin/python3
'''Module creates a unique FileStorage instance for the application

Attrs:
    storage: an instance of FileStorage
'''

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
