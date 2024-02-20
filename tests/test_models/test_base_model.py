#!/usr/bin/python3
"""
Unittest for the BaseModel
"""

import unittest
import time
import datetime
import models
from models.base_model import BaseModel
import inspect
import pycodestyle as pep8
import models.base_model as base_model
from models import db


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_base(self) -> None:
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self) -> None:
        """Test that the test_base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = base_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(BaseModel.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(BaseModel, inspect.ismethod))
        for func in base_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


@unittest.skipIf(db, "not db")
class Test_Base(unittest.TestCase):
    """This class defines unittests for the instantiation of BaseModel class"""

    def test_uniq_time(self):
        """This function tests for the uniquenss of time creation"""
        base1 = BaseModel()
        time.sleep(0.001)
        base2 = BaseModel()
        self.assertNotEqual(base1.created_at, base2.created_at)

    def test_uniq_id(self):
        """This function tests for the uniqueness of the id"""
        base1 = BaseModel()
        base2 = BaseModel()
        self.assertNotEqual(base1.id, base2.id)

    def test_custom_id(self):
        """This function creates a BaseModel eith a specific ID"""
        base = BaseModel()
        base.id = "123456"
        self.assertEqual(base.id, "123456")

    def test_type_id(self):
        """This function tests the type of id attr"""
        self.assertIs(type(BaseModel().id), str)

    def test_type_created_at(self):
        """This function tests the type of created_at attr"""
        self.assertIs(type(BaseModel().created_at), datetime.datetime)

    def test_type_updated_at(self):
        """This function tests for the type of updated_at attr"""
        self.assertIs(type(BaseModel().updated_at), datetime.datetime)

    def test_str(self):
        """This funtion tests string representation of a BaseModel"""
        base = BaseModel()
        base.id = "123456"
        tdy = datetime.datetime.today()
        base.created_at = base.updated_at = tdy
        self.assertIn("[BaseModel] (123456)", base.__str__())
        self.assertIn("'id': '123456'", base.__str__())
        self.assertIn("'created_at': " + repr(tdy), base.__str__())
        self.assertIn("'updated_at': " + repr(tdy), base.__str__())


@unittest.skipIf(db, "not db")
class Test_save(unittest.TestCase):
    """This class tests the instance method save(self)"""

    def test_save(self):
        """This function tests updating the time"""
        base = BaseModel()
        old_time = base.updated_at
        base.save()
        self.assertNotEqual(base.updated_at, old_time)

    def test_two_save(self):
        """This function tests updates the time twice"""
        base = BaseModel()
        first_time = base.updated_at
        base.save()
        self.assertNotEqual(base.updated_at, first_time)
        second_time = base.updated_at
        base.save()
        self.assertNotEqual(base.updated_at, second_time)

    def test_save_args(self):
        """This function give save method an argument"""
        with self.assertRaises(TypeError):
            BaseModel().save("arg")

    def test_save_file(self):
        """This function tests saving into a JSOM file"""
        base = BaseModel()
        base.save()
        with open(models.storage._FileStorage__file_path,
                  encoding="utf-8") as f:
            self.assertIn("BaseModel." + base.id, f.read())


@unittest.skipIf(db, "not db")
class Test_to_dict(unittest.TestCase):
    """unittests for the instance method to_dict"""

    def test_type_dict(self):
        """This function tests the type of to_dict return value"""
        self.assertIs(type(BaseModel().to_dict()), dict)

    def test_contents_dict(self):
        """This function tests the contents of a dictionary"""
        base = BaseModel()
        self.assertIn('updated_at', base.to_dict())
        self.assertIn('__class__', base.to_dict())
        self.assertIn('id', base.to_dict())
        self.assertIn('created_at', base.to_dict())

    def test_dynamic_dict(self):
        """This function tests the dynamic creation of attributes in dict"""
        base = BaseModel()
        base.name = "model"
        base.num = 456
        self.assertIn('name', base.to_dict())
        self.assertIn('num', base.to_dict())

    def test_type_time_in_dict(self):
        """This function tests the type of created_at and updated_at in dict"""
        base = BaseModel()
        base_dict = base.to_dict()
        self.assertIs(type(base_dict['created_at']), str)
        self.assertIs(type(base_dict['updated_at']), str)

    def test_full_dict(self):
        """This function tests creation of a dictionary"""
        base = BaseModel()
        base.id = "123456"
        tdy = datetime.datetime.today()
        base.created_at = base.updated_at = tdy
        dict_base = {'__class__': 'BaseModel',
                     'updated_at': tdy.isoformat(),
                     'created_at': tdy.isoformat(),
                     'id': "123456"}
        self.assertDictEqual(base.to_dict(), dict_base)

    def test_dict_class(self):
        """This function tests that __dict__ repr and to_dict() are
        different"""
        base = BaseModel()
        self.assertNotEqual(base.__dict__, base.to_dict())

    def test_to_dict_arg(self):
        """This function tests giving the instance method to_dict
        arguments"""
        with self.assertRaises(TypeError):
            BaseModel().to_dict("arg")


@unittest.skipIf(db, "not db")
class Test_instantiation(unittest.TestCase):
    """This class defines unittests related to instantiation"""

    def test_init_kwargs(self):
        """This function creates a BaseModel with kwargs"""
        tdy = datetime.datetime.today()
        base = BaseModel(id="123456", created_at=tdy.isoformat(),
                         updated_at=tdy.isoformat())
        self.assertEqual(base.id, "123456")
        self.assertEqual(base.created_at, tdy)
        self.assertEqual(base.updated_at, tdy)

    def test_init_args(self):
        """This function creates a BaseModel without args"""
        td = datetime.datetime.today()
        base = BaseModel("7890", id="4567",
                         created_at=td.isoformat(), updated_at=td.isoformat())
        self.assertEqual(base.id, "4567")
        self.assertEqual(base.created_at, td)
        self.assertEqual(base.updated_at, td)

    def test_wrong_time_format(self):
        """This function tests giving kwargs a wrong time format"""
        tdy = datetime.datetime.today()
        with self.assertRaises(TypeError):
            base = BaseModel(id="12345", created_at=tdy, updated_at=tdy)

    def test_new_storage(self):
        """This function tests the calling of new in instance storage
        during instantiation"""
        base = BaseModel()
        base.save()
        self.assertIn("BaseModel." + base.id, models.storage.all().keys())

    def teat_init_class(self):
        """This function tests giving args a class key"""
        base1 = BaseModel()
        dict_base1 = base1.to_dict()
        dict_base1['__class__'] = "User"
        base2 = BaseModel(**dict_base1)
        dict_base2 = base2.to_dict()
        self.assertEqual(dict_base2['__class__'], "BaseModel")


if __name__ == '__main__':
    unittest.main()
