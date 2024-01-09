#!/usr/bin/env python3
"""The Console module: for interacting with the application backend"""
import cmd
from models import storage
from models.base_model import BaseModel
import re


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
            new.save()
            new = BaseModel()
            print(new.id)

    def do_show(self, arg):
        """prints string repr of instance"""
        args = arg.split()
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
        args = arg.split()
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
