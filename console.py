#!/usr/bin/env python3
"""The Console module: for interacting with the application backend"""
import cmd
from models import storage
from models.base_model import BaseModel


def extract_words(input_string):
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
    modelnames = ('BaseModel')

    def emptyline(self) -> bool:
        return False

    def do_quit(self, arg):
        """Quits the interpreter: QUIT"""
        return True

    def do_EOF(self, arg):
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
