#!/usr/bin/env python3
"""The Console module: for interacting with the application backend"""
import cmd
import re
import os
import json
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def extract_words(input_string):
    """Extracts command arguments from the interpreter correctly.
    This is to allow the use of multiple words in quites as argument."""
    words = []
    in_quotes = False
    current_word = ""

    for char in input_string:
        if char == '"':
            in_quotes = not in_quotes
        elif char.isspace() and not in_quotes:
            if current_word:
                words.append(current_word)
                current_word = ""
        elif char != '"':
            current_word += char

    if current_word:
        words.append(current_word)

    return words


class HBNBCommand(cmd.Cmd):
    """The HBNB command interpreter"""
    prompt = "(hbnb) "
    modelnames = ('Amenity', 'BaseModel', 'City', 'Place',
                  'Review', 'State', 'User')
    cmdnames = ('all', 'destroy', 'show', 'count', 'update')

    def default(self, line):
        """Managing different format of commands"""
        tokens = line.split('.')
        if len(tokens) > 1:
            # target: User.update("uuid", "first_name", "John")
            # Result: ["User", "update", "uuid", "first_name", "John"]
            # target: User.update("bef0b8", {"name": "iyke"})
            # Result: ['User', 'update', '"bef0b8", {"name": "iyke"}']
            mat = re.match(r'^\s*([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)\((.*)\)\s*$',
                           line)
            if mat:
                class_name, command, args = mat.groups()
                if command in self.cmdnames:
                    if re.findall(r"({.*?})", args):  # If args contains a dict
                        # Replace the comma after the id & leave the others
                        args = args.replace(",", "", 1)
                        self.onecmd(f"{command} {class_name} {args}")
                    else:
                        args = ''.join(args.split(','))
                        self.onecmd(f"{command} {class_name} {args}")
                else:
                    print(f"** Invalid command: {line} **")

    def do_count(self, arg):
        """counts number of instances
        <classname>.count()
        """
        objs = storage.all()
        if not arg:
            print("** class name missing **")
        elif arg not in self.modelnames:
            print("** class doesn't exist **")
        else:
            i = 0
            for key, value in objs.items():
                if arg in key:
                    i += 1
            print(i)

    def emptyline(self) -> bool:
        return False

    def do_quit(self, arg):
        """Quits the interpreter:
        quit
        """
        return True

    def do_EOF(self, arg):
        """Quits the interpreter:
        EOF
        """
        print()
        return True

    def do_create(self, arg):
        """creates a new instance of a class:
        create <classname>
        { BaseModel | User | Amenity | City | Review | State | Place }
        """
        if not arg:
            print("** class name missing **")
        elif arg not in self.modelnames:
            print("** class doesn't exist **")
        else:
            new = globals()[arg]()
            new.save()
            print(new.id)

    def do_show(self, arg):
        """prints string repr of instance:
        show <classname> <id>
                or
        <classname>.show(<id>)
        """
        args = extract_words(arg)
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in self.modelnames:
            print(f"** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objs = storage.all()
            if f"{args[0]}.{args[1]}" not in objs.keys():
                print("** no instance found **")
            else:
                print(objs[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """deletes an instance
        destroy <classname> <id>
                or
        <classname>.destroy(<id>)
        """
        args = extract_words(arg)
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in self.modelnames:
            print(f"** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objs = storage.all()
            if f"{args[0]}.{args[1]}" not in objs.keys():
                print("** no instance found **")
            else:
                del objs[f"{args[0]}.{args[1]}"]
                storage.save_changes(objs)

    def do_all(self, arg):
        """prints string repr of instances based or not
on class name:
        all [<classname>]
                or
        <classname>.all()
        """
        objs = storage.all()
        lis = []
        if not arg:
            for key in objs.keys():
                lis.append(str(objs[key]))
        elif arg not in self.modelnames:
            print("** class doesn't exist **")
        else:
            for key, value in objs.items():
                if arg in key:
                    lis.append(str(value))
        print(lis)

    def do_update(self, arg):
        """updates an instance attribute
        update <classname> <id> <attribute> <value>
                            or
        <classname>.update(<id>, <attribute>, <value>)
        """
        if re.findall(r"({.*?})", arg):  # If args contains a dict
            arg = arg.replace("'", "\"")  # Replace any single quotes
        args = extract_words(arg)
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in self.modelnames:
            print(f"** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objs = storage.all()
            if f"{args[0]}.{args[1]}" not in objs.keys():
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:  # NOTE: id, created_at and updated_at aren't updated
                regexp = r"({.*?})"  # dicts only
                matches = re.findall(regexp, arg)
                obj = objs[f"{args[0]}.{args[1]}"]
                if matches:  # UPDATE id {name: John}
                    dict_ = json.loads(matches[0])  # Only 1 dict expected
                    for key, value in dict_.items():
                        # Get the type of the dit item, default type is str
                        type_ = type(dict_.get(key) or "")
                        v = type_(value)
                        setattr(objs[f"{args[0]}.{args[1]}"], key, v)
                else:  # UPDATE id first_name michael
                    type_ = type(getattr(obj, args[2], str))
                    v = type_(args[3])
                    setattr(objs[f"{args[0]}.{args[1]}"], args[2], v)
                storage.save_changes(objs)

    def do_cls(self, arg):
        """clears the screen: CLS"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
