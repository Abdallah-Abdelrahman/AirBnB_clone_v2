#!/usr/bin/python3
"""
Unittest for the console including the class HBNBCommand
"""

import unittest
import models
import os
import json
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


class TestConsole_Base(unittest.TestCase):
    """This class defines unittests for the basic usage of the console"""

    def test_docstr(self):
        """Test class documentaion"""
        self.assertTrue(len(HBNBCommand.__doc__) > 2)

    def test_prompt(self):
        """This function tests having the correct prompt"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_quit_return(self):
        """This function tests the return of onecmd function during quitting"""
        # with patch('sys.stdout', new=StringIO()) as f:
        self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_eof_return(self):
        """This function tests the return of onecmd function during eof"""
        # with patch('sys.stdout', new=StringIO()) as f:
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_invalid_cmd(self):
        """This function tests the output when the class recieves
        invalid cmd"""
        invalid_output = "*** Unknown syntax: arg"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("arg"))
            self.assertEqual(invalid_output, f.getvalue().strip())

    def test_empty_line(self):
        """This function tests recieving an empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", f.getvalue().strip())

    def test_help(self):
        """This function tests the expected output of the command help"""
        cmds = ['EOF', 'all', 'count', 'create', 'destroy',
                'help', 'quit', 'show', 'update']
        expected = ("Documented commands (type help <topic>):\n",
                    "========================================\n",
                    '  '.join(cmds))
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(''.join(expected), f.getvalue().strip())


class TestConsole_help(unittest.TestCase):
    """This class defines unittests for the help method of the console"""

    def test_help_EOF(self):
        """This function tests the <help EOF> message content"""
        expected = "End-of-file"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expected, f.getvalue().strip())

    def test_help_all(self):
        """This function tests the <help all> message content"""
        out = ["Prints all string representation of all instances based or\n",
               "        not on the class name"]
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(''.join(out), f.getvalue().strip())

    def test_help_count(self):
        """This function tests the <help count> message content"""
        out = "Retrives the number of instances of a class"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(out, f.getvalue().strip())

    def test_help_create(self):
        """This function tests the <help create> message content"""
        out = ["Creates a new instance of the class provided, save it into\n",
               "        a JSON file, and prints the id"]
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(''.join(out), f.getvalue().strip())

    def test_help_destroy(self):
        """This function tests the <help destroy> message content"""
        out = "Deletes an instance based on class name and id"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(out, f.getvalue().strip())

    def test_help_help(self):
        """This function tests the <help help> message content"""
        out = ['List available commands with "help" or detailed',
               'help with "help cmd".']
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help help"))
            self.assertEqual(" ".join(out), f.getvalue().strip())

    def test_help_quit(self):
        """This function tests the <help quit> message content"""
        out = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(out, f.getvalue().strip())

    def test_help_show(self):
        """This function tests the <help show> message content"""
        out = ["Prints the string representation of an instance based on\n",
               "        the class and id values"]
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(''.join(out), f.getvalue().strip())

    def test_help_create(self):
        """This function tests the <help update> message content"""
        o = ["Updates an instance based on the class name and id by adding\n",
             "        or updating attributes"]
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(''.join(o), f.getvalue().strip())


class TestConsole_create(unittest.TestCase):
    """This class defines unittests for the create method of the console"""

    @classmethod
    def setUpClass(cls):
        """sets up the environment for testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def tearDown(self):
        """removes files created and resets the value of __objects"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def test_create_invalid(self):
        """This function tests create command with missing class name"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual("** class name missing **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Model"))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_create_invalid_method(self):
        """This function tests create command with missing arguments
        in method format"""
        out1 = "*** Unknown syntax: Model.create()"
        out2 = "*** Unknown syntax: User.create()"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Model.create()"))
            self.assertEqual(out1, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.create()"))
            self.assertEqual(out2, f.getvalue().strip())

    def test_create_cmd_basemodel(self):
        """This method creates a new BaseModel"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with open(models.storage._FileStorage__file_path,
                  encoding="utf-8") as file:
            read_data = file.read()
            self.assertIn("BaseModel." + obj_id, read_data)
        self.assertIn("BaseModel." + obj_id, models.storage.all().keys())

    def test_create_cmd_user(self):
        """This method creates a new User"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with open(models.storage._FileStorage__file_path,
                  encoding="utf-8") as file:
            read_data = file.read()
            self.assertIn("User." + obj_id, read_data)
        self.assertIn("User." + obj_id, models.storage.all().keys())

    def test_create_cmd_city(self):
        """this method creates a new city"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with open(models.storage._FileStorage__file_path,
                  encoding="utf-8") as file:
            read_data = file.read()
            self.assertIn("City." + obj_id, read_data)
        self.assertIn("City." + obj_id, models.storage.all().keys())

    def test_create_cmd_state(self):
        """this method creates a new state"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with open(models.storage._FileStorage__file_path,
                  encoding="utf-8") as file:
            read_data = file.read()
            self.assertIn("State." + obj_id, read_data)
        self.assertIn("State." + obj_id, models.storage.all().keys())

    def test_create_cmd_amenity(self):
        """this method creates a new amenity"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with open(models.storage._FileStorage__file_path,
                  encoding="utf-8") as file:
            read_data = file.read()
            self.assertIn("Amenity." + obj_id, read_data)
        self.assertIn("Amenity." + obj_id, models.storage.all().keys())


class TestConsole_show(unittest.TestCase):
    """This class defines unittests for the create method of the console"""

    @classmethod
    def setUpClass(cls):
        """sets up the environment for testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def tearDown(self):
        """removes files created and resets the value of __objects"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def test_show_invalid(self):
        """This function tests show command with missing class name"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual("** class name missing **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Model"))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Model.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_show_instance_id_missing(self):
        """This function tests every possibility of recieving "id missing"
        msg"""
        msg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("BaseModel.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.show()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_invalid_id(self):
        """This function tests all the possibilities of recieving an
        invalid id msg"""
        msg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd('BaseModel.show("1212121")')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd('User.show("1212121")')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.show('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.show('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.show('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.show('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.show('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_show_objs(self):
        """This function tests the functionality of the show method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel " + obj_id))
            obj = models.storage.all()["BaseModel." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User " + obj_id))
            obj = models.storage.all()["User." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State " + obj_id))
            obj = models.storage.all()["State." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City " + obj_id))
            obj = models.storage.all()["City." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity " + obj_id))
            obj = models.storage.all()["Amenity." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place " + obj_id))
            obj = models.storage.all()["Place." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review " + obj_id))
            obj = models.storage.all()["Review." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel " + obj_id))
            obj = models.storage.all()["BaseModel." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))

    def test_show_method_format(self):
        """This function tests the show method in the dot notation"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("BaseModel.show('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["BaseModel." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.show('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["User." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.show('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["State." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.show('{}') ".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["City." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.show('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["Amenity." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.show('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["Place." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.show('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            obj = models.storage.all()["Review." + obj_id]
            self.assertEqual(f.getvalue().strip(), str(obj))


class TestConsole_destroy(unittest.TestCase):
    """This class defines unittests for the destroy method of the console"""

    @classmethod
    def setUpClass(cls):
        """sets up the environement for testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def tearDown(self):
        """removes files created and resets the value of __objects"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def test_destroy_invalid(self):
        """This function tests destroy command with missing class name"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual("** class name missing **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Model"))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Model.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_destroy_instance_id_missing(self):
        """This function tests every possibility of recieving
        "id missing" msg"""
        msg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("BaseModel.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.destroy()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_invalid_id(self):
        """This function tests all the possibilities of recieving an
        invalid id msg"""
        msg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd('BaseModel.destroy("1212121")')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd('User.destroy("1212121")')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.destroy('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.destroy('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.destroy('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.destroy('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.destroy('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_destroy_objs(self):
        """This function tests the functionality of the destroy method"""
        msg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel " + _id))
            self.assertNotIn("BaseModel." + _id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User " + obj_id))
            self.assertNotIn("User." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State " + obj_id))
            self.assertNotIn("State." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City " + obj_id))
            self.assertNotIn("City." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity " + obj_id))
            self.assertNotIn("Amenity." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place " + obj_id))
            self.assertNotIn("Place." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review " + obj_id))
            self.assertNotIn("Place." + obj_id, models.storage.all())

    def test_destroy_method_format(self):
        """This function tests the destroy method in the dot notation"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            li = HBNBCommand().precmd("BaseModel.destroy('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(li))
            self.assertNotIn("BaseModel." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.destroy('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertNotIn("User." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.destroy('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertNotIn("State." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.destroy('{}') ".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertNotIn("City." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.destroy('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertNotIn("Amenity." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.destroy('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertNotIn("Place." + obj_id, models.storage.all())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.destroy('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertNotIn("Review." + obj_id, models.storage.all())


class TestConsole_all(unittest.TestCase):
    """This class defines unittests for the all method of the console"""

    @classmethod
    def setUpClass(cls):
        """sets up the environment for testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def tearDown(self):
        """removes files created and resets the value of __objects"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def test_all_invalid(self):
        """This function tests all command with missing class name"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Model"))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Model.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_all_objs(self):
        """This function tests the functionality of the all method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", f.getvalue().strip())
            self.assertIn("User", f.getvalue().strip())
            self.assertIn("State", f.getvalue().strip())
            self.assertIn("City", f.getvalue().strip())
            self.assertIn("Amenity", f.getvalue().strip())
            self.assertIn("Place", f.getvalue().strip())
            self.assertIn("Review", f.getvalue().strip())

    def test_all_cls(self):
        """This function tests the functionality of all with arg method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertTrue(all("BaseModel" in d_ for d_ in list_obj))
            self.assertIs(type(list_obj), list)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("User" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("State" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("City" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("Amenity" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("Place" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("Review" in d_ for d_ in list_obj))

    def test_all_cls_method(self):
        """This function tests the functionality of all with arg method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("BaseModel.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("BaseModel", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertTrue(all("BaseModel" in d_ for d_ in list_obj))
            self.assertIs(type(list_obj), list)
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("User", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("User" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("State", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("State" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("City", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("City" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("Amenity", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("Amenity" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("Place", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("Place" in d_ for d_ in list_obj))
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertIn("Review", f.getvalue().strip())
            list_obj = json.loads(f.getvalue().strip())
            self.assertIs(type(list_obj), list)
            self.assertTrue(all("Review" in d_ for d_ in list_obj))


class TestConsole_update(unittest.TestCase):
    """This class defines unittests for the update method of the console"""

    @classmethod
    def setUpClass(cls):
        """This is a set up class for the update class"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def tearDown(self):
        """removes files created and resets the value of __objects"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        models.storage._FileStorage__objects = {}

    def test_update_invalid(self):
        """This function tests update command with missing class name"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual("** class name missing **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Model"))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Model.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_update_instance_id_missing(self):
        """This function tests every possibility of recieving
        "id missing" msg"""
        msg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("BaseModel.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.update()")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_invalid_id(self):
        """This function tests all the possibilities of recieving an
        invalid id msg"""
        msg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update State 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update City 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Place 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Review 1212121"))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd('BaseModel.update("1212121")')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd('User.update("1212121")')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.update('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.update('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.update('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.update('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.update('1212121')")
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_update_missing_name(self):
        """This function tests the functionality of the update method"""
        msg = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel " + _id))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User " + obj_id))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update State " + obj_id))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update City " + obj_id))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Amenity " + obj_id))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Place " + obj_id))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Review " + obj_id))
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_missing_name_method(self):
        """This function tests the update method in the dot notation"""
        msg = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            li = HBNBCommand().precmd("BaseModel.update('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(li))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("User.update('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("State.update('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("City.update('{}') ".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Amenity.update('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Place.update('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            line = HBNBCommand().precmd("Review.update('{}')".format(obj_id))
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_missing_value(self):
        """This function tests the functionality of the update method"""
        msg = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update BaseModel " + _id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update User " + obj_id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update State " + obj_id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update City " + obj_id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update Amenity " + obj_id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update Place " + obj_id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "update Review " + obj_id + " value"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_missing_value_method(self):
        """This function tests the update method in the dot notation"""
        msg = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "BaseModel.update('{}' name)".format(obj_id)
            li = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(li))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "User.update('{}', 'name')".format(obj_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "State.update('{}', 'name')".format(obj_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "City.update('{}', 'name')".format(obj_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "Amenity.update('{}', 'name')".format(obj_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "Place.update('{}', 'name')".format(obj_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            obj_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "Review.update('{}', 'name')".format(obj_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_objs(self):
        """This function tests the functionality of the update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        cmd = "update BaseModel " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        attr = models.storage.all()["BaseModel." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        cmd = "update User " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        attr = models.storage.all()["User." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            _id = f.getvalue().strip()
        cmd = "update State " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        attr = models.storage.all()["State." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            _id = f.getvalue().strip()
        cmd = "update City " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        attr = models.storage.all()["City." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            _id = f.getvalue().strip()
        cmd = "update Amenity " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn("name", models.storage.all()["Amenity." + _id].__dict__)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "update Place " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        attr = models.storage.all()["Place." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            _id = f.getvalue().strip()
        cmd = "update Review " + _id + " name" + " value"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        attr = models.storage.all()["Review." + _id].__dict__
        self.assertIn("name", attr)

    def test_update_objs_method(self):
        """This function tests the functionality of the update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        cmd = "BaseModel.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["BaseModel." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        cmd = "User.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["User." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            _id = f.getvalue().strip()
        cmd = "State.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["State." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            _id = f.getvalue().strip()
        cmd = "City.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["City." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            _id = f.getvalue().strip()
        cmd = "Amenity.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Amenity." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "Place.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Place." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            _id = f.getvalue().strip()
        cmd = "Review.update('{}', 'name', 'value')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Review." + _id].__dict__
        self.assertIn("name", attr)

    def test_update_int_method(self):
        """This function checks certain functionalities of update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "update Place " + _id + " number_rooms" + " '7'"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        _dict = models.storage.all()["Place." + _id].__dict__
        self.assertIs(type(_dict["number_rooms"]), int)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "Place.update('{}', 'number_rooms', \"7\")".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Place." + _id].__dict__
        self.assertIs(type(_dict["number_rooms"]), int)

    def test_update_float_method(self):
        """This function checks certain functionalities of update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "update Place " + _id + " latitude" + " 3.9"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        _dict = models.storage.all()["Place." + _id].__dict__
        self.assertIs(type(_dict["latitude"]), float)

    def test_string_quotes_update(self):
        """This function tests certain functionalies of update function"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        cmd = "update User " + _id + " first_name" + " 'John Doe'"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        _dict = models.storage.all()["User." + _id].__dict__
        self.assertEqual(_dict['first_name'], "John Doe")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        cmd = "User.update('{}', 'first_name', 'John Doe')".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        _dict = models.storage.all()["User." + _id].__dict__
        self.assertEqual(_dict['first_name'], "John Doe")

    def test_update_dict(self):
        """This function tests the functionality of update with a dict
        passed"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        cmd = "BaseModel.update('{}', {{'first_name': 'John'}}".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["BaseModel." + _id].__dict__
        self.assertIn("first_name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        cmd = "User.update('{}', {{'name': 'value'}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["User." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            _id = f.getvalue().strip()
        cmd = "State.update('{}', {{'name': 'value'}}".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["State." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            _id = f.getvalue().strip()
        cmd = "City.update('{}', {{'name': 'value'}}".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["City." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            _id = f.getvalue().strip()
        cmd = "Amenity.update('{}', {{'name': 'value'}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Amenity." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "Place.update('{}', {{'name': 'value'}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Place." + _id].__dict__
        self.assertIn("name", attr)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            _id = f.getvalue().strip()
        cmd = "Review.update('{}', {{'name': 'value'}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        attr = models.storage.all()["Review." + _id].__dict__
        self.assertIn("name", attr)

    def test_update_invalid_dict(self):
        """This function tests for the response of update to invalid dict"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "BaseModel.update('{}', {{'first_name', 'John'}}".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "User.update('{}', {{'name', 'value'}})".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "State.update('{}', {{'name', 'value'}}".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            attr = models.storage.all()["State." + _id].__dict__
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "City.update('{}', {{'name', 'value'}}".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "Amenity.update('{}', {{'name', 'value'}}".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "Place.update('{}', {{'name', 'value'}}".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            _id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd = "Review.update('{}', {{'name' 'value'}})".format(_id)
            line = HBNBCommand().precmd(cmd)
            self.assertFalse(HBNBCommand().onecmd(line))
            msg = "*** Unknown syntax: " + cmd
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_int_method_dict(self):
        """This function checks certain functionalities of update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "Place.update('{}', {{'number_rooms': \"7\"}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        _dict = models.storage.all()["Place." + _id].__dict__
        self.assertIs(type(_dict["number_rooms"]), int)

    def test_update_float_method_dict(self):
        """This function checks certain functionalities of update method"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            _id = f.getvalue().strip()
        cmd = "Place.update('{}', {{'latitude': 3.9}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        _dict = models.storage.all()["Place." + _id].__dict__
        self.assertIs(type(_dict["latitude"]), float)

    def test_string_quotes_update_dict(self):
        """This function tests certain functionalies of update function"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            _id = f.getvalue().strip()
        cmd = "User.update('{}', {{'first_name': 'John Doe'}})".format(_id)
        line = HBNBCommand().precmd(cmd)
        self.assertFalse(HBNBCommand().onecmd(line))
        _dict = models.storage.all()["User." + _id].__dict__
        self.assertEqual(_dict['first_name'], "John Doe")


class Test_count(unittest.TestCase):
    '''class test counting the number of intances'''
    @classmethod
    def setUpClass(cls):
        '''Remove the file at the begining of the test'''
        models.FileStorage._FileStorage__objects = {}
        try:
            os.remove(models.FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def setUp(self):
        '''Reset the `FileStorage.__objects`'''
        models.FileStorage._FileStorage__objects = {}
        try:
            os.remove(models.FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def test_count_zero(self):
        '''Test there's number of counting instances printed'''
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count'))
            self.assertTrue(f.getvalue().strip().isnumeric())
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count BaseModel'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count User'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count City'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count Amenity'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count Review'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count State'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count Place'))
            self.assertEqual(int(f.getvalue().strip()), 0)

    def test_count_BaseModel(self):
        '''Test there's number of counting instances printed'''
        from models.base_model import BaseModel
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count BaseModel'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            BaseModel()
            line = HBNBCommand().precmd('BaseModel.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_User(self):
        '''Test count User'''
        from models.user import User
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count User'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            User()
            line = HBNBCommand().precmd('User.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_City(self):
        '''Test count City'''
        from models.city import City
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count City'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            City()
            line = HBNBCommand().precmd('City.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_Amenity(self):
        '''Test count Amenity'''
        from models.amenity import Amenity
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count Amenity'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            Amenity()
            line = HBNBCommand().precmd('Amenity.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_State(self):
        '''Test count State'''
        from models.state import State
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count State'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            State()
            line = HBNBCommand().precmd('State.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_Review(self):
        '''Test count Review'''
        from models.review import Review
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count Review'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            Review()
            line = HBNBCommand().precmd('Review.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_Place(self):
        '''Test count Place'''
        from models.place import Place
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count Place'))
            self.assertEqual(int(f.getvalue().strip()), 0)
        with patch("sys.stdout", new=StringIO()) as f:
            Place()
            line = HBNBCommand().precmd('Place.count()')
            self.assertFalse(HBNBCommand().onecmd(line))
            self.assertEqual(int(f.getvalue().strip()), 1)

    def test_count_arg(self):
        '''Invalid arg'''
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('count arg'))
            self.assertEqual(int(f.getvalue().strip()), 0)


if __name__ == '__main__':
    unittest.main()
