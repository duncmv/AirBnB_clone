#!/usr/bin/env python3
"""The Console module: for interacting with the application backend"""
import cmd


class HBNBCommand(cmd.Cmd):
    """The HBNB command interpreter class"""
    prompt = "(hbnb) "

    def emptyline(self) -> bool:
        return False

    def do_quit(self, arg):
        """Quits the interpreter: QUIT"""
        return True

    def do_EOF(self, arg):
        """Quits the interpreter: EOF"""
        print()
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
