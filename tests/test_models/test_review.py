#!/usr/bin/python3
"""
Unittest for the Class "Review"
"""

import io
import unittest
import datetime
import uuid
import models
from unittest.mock import patch
from models.review import Review
import inspect
import pycodestyle as pep8
import models.review as review_model
from models import db


class TestReviewDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_review(self) -> None:
        """Test that the review_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_review(self) -> None:
        """Test that the test_review_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = review_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(Review.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        review_funcs = inspect.getmembers(Review, inspect.isfunction)
        review_funcs.extend(inspect.getmembers(Review, inspect.ismethod))
        for func in review_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


@unittest.skipIf(db, "not db")
class Test_Review(unittest.TestCase):
    '''Test Review class'''
    def test_docstr(self):
        '''Test class documentaion'''
        self.assertTrue(len(Review.__doc__) > 2)

    def test_init(self):
        '''Test instances/cls attrs exists'''
        rev = Review()
        # instance attrs
        self.assertTrue(hasattr(rev, 'id'))
        self.assertTrue(hasattr(rev, 'created_at'))
        self.assertTrue(hasattr(rev, 'updated_at'))
        # cls attrs
        self.assertTrue(hasattr(rev, 'place_id'))
        self.assertTrue(hasattr(rev, 'user_id'))
        self.assertTrue(hasattr(rev, 'text'))

    def test_type_attrs(self):
        '''Test instance types'''
        rev = Review()
        # instance attrs
        self.assertIsInstance(rev.id, str)
        self.assertIsInstance(rev.created_at, datetime.datetime)
        self.assertIsInstance(rev.updated_at, datetime.datetime)
        # cls attrs
        self.assertIsInstance(rev.place_id, str)
        self.assertIsInstance(rev.user_id, str)
        self.assertIsInstance(rev.text, str)

    def test_args(self):
        '''Test anonymous arguments'''
        id = str(uuid.uuid4())
        rev = Review(id)
        self.assertNotEqual(id, rev.id)

    def test_kwargs(self):
        '''Test named arguments'''
        kw = {
                'id': 1, 'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now()
             }
        with self.assertRaises(TypeError):
            Review(**kw)
        kw['created_at'] = datetime.datetime.now().isoformat()
        kw['updated_at'] = datetime.datetime.now().isoformat()
        rev = Review(**kw)
        self.assertEqual(rev.id, kw['id'])
        self.assertEqual(rev.created_at.isoformat(), kw['created_at'])
        self.assertEqual(rev.updated_at.isoformat(), kw['updated_at'])

    def test_save(self):
        '''Test saving object to file.json'''
        rev = Review()
        prev_date = rev.updated_at
        rev.save()
        curr_date = rev.updated_at
        self.assertIn('Review'+'.'+rev.id,
                      models.FileStorage._FileStorage__objects)
        self.assertNotEqual(prev_date.isoformat(), curr_date.isoformat())
        with self.assertRaises(TypeError):
            rev.save('')

    def test_to_dict(self):
        '''Test `to_dict` method'''
        rev = Review()
        dct = rev.to_dict()
        self.assertIn('__class__', dct)
        self.assertEqual('Review', dct['__class__'])
        with self.assertRaises(TypeError):
            rev.to_dict({'id': '123'})
            Review()

    def test_str(self):
        '''Test `Review` representaion'''
        with patch('sys.stdout', new_callable=io.StringIO) as m_stdout:
            rev = Review()
            print(rev)
            self.assertEqual(m_stdout.getvalue(),
                             '[Review] ({}) {}\n'.format(rev.id, rev.__dict__))


if __name__ == '__main__':
    unittest.main()
