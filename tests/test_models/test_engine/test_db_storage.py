#!/usr/bin/python3
"""
Unittest for the DBStorage Class
"""

import unittest
import datetime
import os
import models
from models.engine import db_storage
from models.engine.db_storage import DBStorage
import inspect
import pycodestyle as pep8
from models import storage, db
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import MySQLdb


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for FileStorage class
    documentation and pep8 conformaty"""
    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_file_storage conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_engine/' +
                                    'test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = db_storage.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation"""
        mod_doc = str(DBStorage.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(DBStorage, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(DBStorage, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


def create_cursor():
    """Create a cursor"""
    conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                           port=3306,
                           user=os.getenv('HBNB_MYSQL_USER'),
                           passwd=os.getenv('HBNB_MYSQL_PWD'),
                           db=os.getenv('HBNB_MYSQL_DB'))
    return conn.cursor()


@unittest.skipIf(not db, "db")
class TestDBStorage(unittest.TestCase):
    """Test for the DBStorage class"""
    def setUp(self):
        self.storage = storage
        self.instances = {}
        self.instances['State'] = State(name="California")
        self.instances['City'] = City(name="San Francisco",
                                      state_id=self.instances['State'].id)
        self.instances['User'] = User(email="user@mail.com", password="123",
                                      name="John", last_name="Doe")
        self.instances['Place'] = Place(name="House",
                                        city_id=self.instances['City'].id,
                                        user_id=self.instances['User'].id)
        self.instances['Review'] = Review(text="Great place",
                                          place_id=self.instances['Place'].id,
                                          user_id=self.instances['User'].id)
        self.instances['Amenity'] = Amenity(name="Wifi")
        self.instances['Place'].amenities.append(self.instances['Amenity'])
        for instance in self.instances.values():
            instance.save()
        self.storage.save()
        self.cursor = create_cursor()

    def tearDown(self):
        """Tear down the tests"""
        ignore = ['City', 'Review', 'Place']
        for k, instance in self.instances.items():
            if k not in ignore:
                instance.delete()
        self.storage.save()
        self.cursor.close()

    def test_methods_exist(self):
        '''Test the db storage has certain methods'''
        methods = ['save', 'all', 'new', 'reload', 'delete']

        self.assertIsInstance(storage, DBStorage)
        funcs = [f[0] for f in inspect.getmembers(DBStorage,
                                                  inspect.isfunction)]
        for m in methods:
            self.assertIn(m, funcs)

    def test_all(self):
        """Test the all method"""
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertEqual(len(all_objs), len(self.instances))

    def test_new(self):
        """Test the new method"""
        all_objs = self.storage.all(State)
        self.cursor.execute("SELECT * FROM states")
        self.assertEqual(len(all_objs), self.cursor.rowcount)
        new_state = State(name="New York")
        new_state.save()
        self.instances['State2'] = new_state
        all_objs = self.storage.all(State)
        self.assertIn(new_state, all_objs.values())
        self.cursor.execute("SELECT * FROM states")
        self.assertEqual(len(all_objs) - self.cursor.rowcount, 1)

    def test_save(self):
        """Test the save method"""
        new_state = State(name="New York")
        new_state.save()
        self.instances['State3'] = new_state
        self.storage.save()
        self.cursor.close()
        self.cursor = create_cursor()
        self.cursor.execute("SELECT * FROM states")
        self.assertEqual(len(self.storage.all(State)), self.cursor.rowcount)

    def test_delete(self):
        """Test the delete method"""
        self.instances['del_state'] = State(name="Texas")
        self.instances['del_state'].save()
        del_id = self.instances['del_state'].id
        self.cursor.close()
        self.cursor = create_cursor()
        self.cursor.execute("SELECT * FROM states WHERE id='{}'"
                            .format(del_id))
        self.assertEqual(self.cursor.rowcount, 1)
        self.storage.delete(self.instances['del_state'])
        self.storage.save()
        self.cursor.close()
        self.cursor = create_cursor()
        self.cursor.execute("SELECT * FROM states WHERE id='{}'"
                            .format(del_id))
        self.assertEqual(self.cursor.rowcount, 0)
        self.assertNotIn(self.instances['del_state'],
                         self.storage.all(State).values())
        del self.instances['del_state']

    def test_reload(self):
        """Test the reload method"""
        from sqlalchemy.orm.session import Session
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertEqual(len(all_objs), len(self.instances))


@unittest.skipIf(not db, "db")
class TestDBStorageRelations(unittest.TestCase):
    '''Test relations between classes that
    mpas to tables in SQLAlchemy.
    '''

    def setUp(self):
        '''Runs before each test method'''
        self.storage = storage
        self.instances = {}
        self.instances['State'] = State(name="California")
        self.instances['City'] = City(name="San Francisco",
                                      state_id=self.instances['State'].id)
        self.instances['User'] = User(email="user@mail.com", password="123",
                                      name="John", last_name="Doe")
        self.instances['Place'] = Place(name="House",
                                        city_id=self.instances['City'].id,
                                        user_id=self.instances['User'].id)
        self.instances['Review'] = Review(text="Great place",
                                          place_id=self.instances['Place'].id,
                                          user_id=self.instances['User'].id)
        self.instances['Amenity'] = Amenity(name="Wifi")
        self.instances['Place'].amenities.append(self.instances['Amenity'])
        for instance in self.instances.values():
            instance.save()
        self.storage.save()
        self.cursor = create_cursor()

    def tearDown(self):
        '''Runs after each test'''
        ignore = ['City', 'Review', 'Place']
        for k, instance in self.instances.items():
            if k not in ignore:
                instance.delete()
        self.storage.save()
        self.cursor.close()

    def test_relation_State_City(self):
        '''Test relations between State and City tables'''
        cities = self.instances['State'].cities
        for city in cities:
            self.assertEqual(city.state_id, self.instances['State'].id)
            self.assertEqual(city.state, self.instances['State'])
            self.assertEqual(city.name, self.instances['City'].name)
            self.assertEqual(city.id, self.instances['City'].id)

    def test_relation_City_Place_Amenity(self):
        '''Test relations between tables City, Place and Amenity'''
        places = self.instances['City'].places
        for place in places:
            self.assertEqual(place.city_id, self.instances['City'].id)
            self.assertEqual(place.name, self.instances['Place'].name)
            self.assertEqual(place.id, self.instances['Place'].id)
            for amenity in place.amenities:
                self.assertIn(amenity, self.instances['Place'].amenities)

    def test_relation_User_Place_Review(self):
        '''Test relations between tables User, Place and Review'''
        import warnings
        from sqlalchemy.exc import SAWarning
        warnings.simplefilter('ignore', category=SAWarning)
        reviews_user = self.instances['User'].reviews
        reviews_place = self.instances['Place'].reviews
        self.assertEqual(reviews_user, reviews_place)
        for review in reviews_user:
            self.assertEqual(review.user_id, self.instances['User'].id)
            self.assertEqual(review.place_id, self.instances['Place'].id)
            self.assertEqual(review.text, self.instances['Review'].text)
            self.assertEqual(review.id, self.instances['Review'].id)

    # def test_relation_failure(self):
    #     '''Test relations between tables are not well set'''
    #     from sqlalchemy.exc import PendingRollbackError, OperationalError
    #     from io import StringIO as StringIO
    #     from unittest.mock import patch

    #     self.instances['Place1'] = Place(name="San")
    #     with patch("sys.stderr", new=StringIO()) as _:
    #         with self.assertRaises((PendingRollbackError,
    #                                 MySQLdb.OperationalError,
    #                                 OperationalError)):
    #             self.instances['Place1'].save()
    #     self.storage.rollback()
    #     del self.instances['Place1']


if __name__ == '__main__':
    unittest.main()
