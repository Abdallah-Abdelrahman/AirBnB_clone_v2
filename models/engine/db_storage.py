#!/usr/bin/python3
"""db_storage module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

env = ['HBNB_MYSQL_USER', 'HBNB_MYSQL_PWD',
       'HBNB_MYSQL_HOST', 'HBNB_MYSQL_DB',
       'HBNB_TYPE_STORAGE', 'HBNB_ENV']

classes = [User, State, City, Place, Review, Amenity]


class DBStorage:
    """DBStorage class

    Attributes:

    Methods:
    """
    __engine = None
    __session = None

    def __init__(self):
        """initialize engine
        """
        MYSQL = {}
        for e in env:
            MYSQL[e.split('_')[-1]] = getenv(e)
        # dialect+driver://username:password@host:port/database
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(MYSQL['USER'], MYSQL['PWD'],
                                              MYSQL['HOST'], MYSQL['DB']),
                                      pool_pre_ping=True)
        if MYSQL['ENV'] == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))()

    def all(self, cls=None):
        """query on the current database session
        """
        res = {}
        objs = []
        if cls:
            # list of dictionaries
            objs = self.__session.query(cls).all()
        else:
            for c in classes:
                objs.extend(self.__session.query(c).all())

        if objs:
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                res[key] = obj
        return res

    def new(self, obj):
        """add object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current db session if obj is not none
        """
        if obj:
            self.__session.delete(obj)
