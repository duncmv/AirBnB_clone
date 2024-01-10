#!/usr/bin/env python3
"""The Console module: for interacting with the application backend"""
import cmd
import os
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
    """The HBNB command interpreter class"""
    prompt = "(hbnb) "
    modelnames = ('Amenity', 'BaseModel', 'City', 'Place',
                  'Review', 'State', 'User')

    def do_help(self, arg: str) -> bool:
        """Overrides the default help to provide help for
        the extra or secondary commands. If no such help is found,
        the default is made to proceed by returning True.
        This means that search helper functions must return True
        to make do_help know this."""
        if arg.lower().startswith("user"):
            ret = User.user_help(arg)
            if type(ret) is bool and ret is True:
                return super().do_help(arg)
            return ret
        return super().do_help(arg)

    def get_other_handler(self, line):
        """Returns the handler of a secondary command if available"""
        sec_cmds = SecondaryCommands()
        command = line.split(".")[0].lower()
        if hasattr(sec_cmds, command):
            return getattr(sec_cmds, command)
        return None

    def default(self, line: str) -> bool:
        """Overrides the default to allow/support extra commands.
        If te override handler returns True, it means that no proper handler
        for found for the input. So returning True tells default to proceed
        execution to the super class' default handling"""
        handler = self.get_other_handler(line)
        if handler and callable(handler):
            ret = handler(line)
            if type(ret) is bool and ret is True:  # Proceed to default action
                return super().do_help(line)
            return ret
        return super().do_help(line)

    def emptyline(self) -> bool:
        """Overrides the default to prevent re-run of last command"""
        return False

    def do_quit(self, arg):
        """Quits the interpreter: QUIT"""
        return True

    def do_EOF(self, arg: str):
        """Quits the interpreter: EOF"""
        print()
        return True

    def do_create(self, arg):
        """creates a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
        elif arg not in self.modelnames:
            print("** class doesn't exist **")
        else:
            new = globals()[arg]()
            new.save()
            print(new.id)

    def do_show(self, arg):
        """prints string repr of instance"""
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
        """deletes an instance"""
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
on class name"""
        objs = storage.all()
        if not arg:
            for key in objs.keys():
                print(objs[key])
        elif arg not in self.modelnames:
            print("** class doesn't exist **")
        else:
            for key, value in objs.items():
                if arg in key:
                    print(value)

    def do_update(self, arg):
        """updates an instance attribute"""
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
            else:
                setattr(objs[f"{args[0]}.{args[1]}"], args[2], args[3])
                storage.save_changes(objs)


class SecondaryCommands:
    """The SecondaryCommands class: for other commands command"""

    def exit(self, arg):
        """Another way to quit: EXIT"""
        return True

    def cls(self, arg):
        """Clear the screen if you will: CLS"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def user(self, arg):
        """User related commands: User.all"""

        array = arg.split(".")

        # Method exists on User? Then call it with any arguments given
        if (callable(len(array) > 1 and getattr(User, array[1], None))):
            getattr(User, array[1], None)(".".join(array[2:]))
            return
        return True  # Proceed to the super class' default handling


if __name__ == "__main__":
    HBNBCommand().cmdloop()
