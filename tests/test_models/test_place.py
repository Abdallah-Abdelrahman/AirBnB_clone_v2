#!/usr/bin/python3
"""
Unittest for the Class "Place"
"""

import io
import unittest
import datetime
import uuid
import models
from unittest.mock import patch
from models.place import Place
import inspect
import pycodestyle as pep8
import models.place as place_model


class TestPlaceDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_place(self) -> None:
        """Test that the place_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_place(self) -> None:
        """Test that the test_place_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = place_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(Place.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        place_funcs = inspect.getmembers(Place, inspect.isfunction)
        place_funcs.extend(inspect.getmembers(Place, inspect.ismethod))
        for func in place_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class Test_Place(unittest.TestCase):
    '''Test Place class'''
    def test_docstr(self):
        '''Test class documentaion'''
        self.assertTrue(len(Place.__doc__) > 2)

    def test_init(self):
        '''Test instances/cls attrs exists'''
        rev = Place()
        # instance(default) attrs
        self.assertTrue(hasattr(rev, 'id'))
        self.assertTrue(hasattr(rev, 'created_at'))
        self.assertTrue(hasattr(rev, 'updated_at'))
        # cls attrs
        self.assertTrue(hasattr(rev, 'city_id'))
        self.assertTrue(hasattr(rev, 'user_id'))
        self.assertTrue(hasattr(rev, 'name'))
        self.assertTrue(hasattr(rev, 'description'))
        self.assertTrue(hasattr(rev, 'number_rooms'))
        self.assertTrue(hasattr(rev, 'number_rooms'))
        self.assertTrue(hasattr(rev, 'number_bathrooms'))
        self.assertTrue(hasattr(rev, 'price_by_night'))
        self.assertTrue(hasattr(rev, 'latitude'))
        self.assertTrue(hasattr(rev, 'longitude'))
        self.assertTrue(hasattr(rev, 'amenity_ids'))

    def test_type_attrs(self):
        '''Test instance types'''
        rev = Place()
        # instance attrs
        self.assertIsInstance(rev.id, str)
        # cls attrs
        self.assertIsInstance(rev.city_id, str)
        self.assertIsInstance(rev.user_id, str)
        self.assertIsInstance(rev.name, str)
        self.assertIsInstance(rev.description, str)
        self.assertIsInstance(rev.number_rooms, int)
        self.assertIsInstance(rev.number_bathrooms, int)
        self.assertIsInstance(rev.max_guest, int)
        self.assertIsInstance(rev.price_by_night, int)
        self.assertIsInstance(rev.latitude, float)
        self.assertIsInstance(rev.longitude, float)
        self.assertIsInstance(rev.amenity_ids, list)
        self.assertTrue(all(isinstance(id, str) for id in rev.amenity_ids))

    def test_args(self):
        '''Test anonymous arguments'''
        id = str(uuid.uuid4())
        rev = Place(id)
        self.assertNotEqual(id, rev.id)

    def test_kwargs(self):
        '''Test named arguments'''
        kw = {
                'id': 1, 'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now(),
             }
        # invalid date format
        with self.assertRaises(TypeError):
            Place(**kw)
        kw['created_at'] = datetime.datetime.now().isoformat()
        kw['updated_at'] = datetime.datetime.now().isoformat()
        rev = Place(**kw)
        self.assertEqual(rev.id, kw['id'])
        self.assertEqual(rev.created_at.isoformat(), kw['created_at'])
        self.assertEqual(rev.updated_at.isoformat(), kw['updated_at'])
        # TODO: validate the type of predefined attrs
        # self.assertEqual(rev.number_rooms, 3)
        # self.assertIsInstance(rev.number_rooms, int)

    def test_save(self):
        '''Test saving object to file.json'''
        rev = Place()
        prev_date = rev.updated_at
        rev.save()
        curr_date = rev.updated_at
        self.assertIn('Place'+'.'+rev.id,
                      models.FileStorage._FileStorage__objects)
        self.assertNotEqual(prev_date.isoformat(), curr_date.isoformat())
        with self.assertRaises(TypeError):
            rev.save('')

    def test_to_dict(self):
        '''Test `to_dict` method'''
        rev = Place()
        dct = rev.to_dict()
        self.assertIn('__class__', dct)
        self.assertEqual('Place', dct['__class__'])
        with self.assertRaises(TypeError):
            rev.to_dict({'id': '123'})
            Place()

    def test_str(self):
        '''Test `Place` representaion'''
        with patch('sys.stdout', new_callable=io.StringIO) as m_stdout:
            rev = Place()
            print(rev)
            self.assertEqual(m_stdout.getvalue(),
                             '[Place] ({}) {}\n'.format(rev.id, rev.__dict__))


if __name__ == '__main__':
    unittest.main()
