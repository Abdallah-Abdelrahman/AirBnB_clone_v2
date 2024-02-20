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
from models.place import Place, place_amenity
from models.review import Review
from models.amenity import Amenity


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

    def tearDown(self):
        """Tear down the tests"""
        ignore = ['City', 'Review', 'Place']
        for k, instance in self.instances.items():
            if k not in ignore:
                instance.delete()
        self.storage.save()

    def test_all(self):
        """Test the all method"""
        print("test_all")
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertEqual(len(all_objs), len(self.instances))

    def test_new(self):
        """Test the new method"""
        print("test_new")
        new_state = State(name="New York")
        new_state.save()
        self.instances['State2'] = new_state
        all_objs = self.storage.all()
        self.assertIn(new_state, all_objs.values())


if __name__ == '__main__':
    unittest.main()
