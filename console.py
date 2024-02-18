#!/usr/bin/python3
"""Entry point of the command interpreter
Defines `HBNBCommand` class that inherits from
`cmd.Cmd`
"""

import re
import cmd
import shlex
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand which acts as the console of the AirBNB clone
    which is a command interpreter to manipulate data without visual
    interface.

    Attrs:
        prompt(str): prompt string
        cls(dict): dictionary of all the instances.
    """

    prompt = "(hbnb) "
    cls = {
            "BaseModel": BaseModel, "User": User, "State": State,
            "City": City, "Amenity": Amenity, "Place": Place, "Review": Review
          }

    def precmd(self, line):
        """This function intervenes and rewrites the command or simply
        just return it unchanged"""

        cmds = [".all", ".count", ".show", ".destroy", ".update"]
        group1 = r'(?<=\.)[^(]+|[aA-zZ]+(?=\.)'
        group2 = r'(?<=\(\"|\(\')[a-z0-9\-]+'
        group3 = r'(?<=\"|\')[\w\s\d]+|\d+(?=[\)\s]+)'
        regx = group1 + '|' + group2 + '|' + group3
        if any(cmd in line for cmd in cmds):
            _dict = re.search(r'{.+}', line)
            if _dict:
                try:
                    dct = json.loads(_dict.group().replace("'", '"'))
                    args = re.findall(group1 + '|' + group2, line)
                    for k, v in dct.items():
                        self.do_update('{} {} {} "{}"'.
                                       format(args[0], args[2], k, v))
                    return ''
                except Exception:
                    return line

            args = re.findall(regx, line)
            args[0], args[1] = args[1], args[0]
            return ' '.join('"'+w+'"' if ' ' in w else w for w in args)

        return line

    def emptyline(self):
        """Handle empty line by doing nothing"""
        pass

    def do_quit(self, _):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, _):
        """End-of-file"""
        return True

    def do_create(self, line):
        """
        Creates a new instance of the class provided, save it into
        a JSON file, and prints the id
        """
        line = line.split(" ")
        if not len(line[0]):
            print("** class name missing **")
            return
        elif line[0] not in self.cls:
            print("** class doesn't exist **")
            return
        obj = self.cls[line[0]]()
        storage.save()
        print(obj.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance based on
        the class and id values
        """

        line = line.split(" ")
        if not len(line[0]):
            print("** class name missing **")
            return
        elif line[0] not in self.cls:
            print("** class doesn't exist **")
            return
        elif len(line) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(line[0], line[1])
        obj_dict = storage.all()
        if key not in obj_dict:
            print("** no instance found **")
            return
        print(obj_dict[key])

    def do_destroy(self, line):
        """Deletes an instance based on class name and id"""
        line = line.split(" ")
        if not len(line[0]):
            print("** class name missing **")
            return
        elif line[0] not in self.cls:
            print("** class doesn't exist **")
            return
        elif len(line) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(line[0], line[1])
        obj_dict = storage.all()
        if key not in obj_dict:
            print("** no instance found **")
            return
        obj_dict.pop(key)
        storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances based or
        not on the class name
        """
        line = line.split(" ")
        if len(line[0]) and line[0] not in self.cls:
            print("** class doesn't exist **")
            return
        obj_dict = storage.all()
        if not len(line[0]):
            print(list(map(lambda x: str(x), obj_dict.values())))
            return
        cls_list = [str(v) for k, v in obj_dict.items() if line[0] in k]
        print(cls_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding
        or updating attributes
        """
        line = shlex.split(line)
        if not line:
            print("** class name missing **")
            return
        elif line[0] not in self.cls:
            print("** class doesn't exist **")
            return
        elif len(line) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(line[0], line[1])
        obj_dict = storage.all()
        if key not in obj_dict:
            print("** no instance found **")
            return
        if len(line) == 2:
            print("** attribute name missing **")
            return
        if len(line) == 3:
            print("** value missing **")
            return
        obj = obj_dict[key]
        if hasattr(obj, line[2]):
            type_attr = type(getattr(obj, line[2]))
            line[3] = type_attr(line[3])
        setattr(obj, line[2], line[3])
        storage.save()

    def do_count(self, line):
        """Retrives the number of instances of a class"""
        count = 0
        obj_dict = storage.all()
        for key in obj_dict:
            if line in key:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
