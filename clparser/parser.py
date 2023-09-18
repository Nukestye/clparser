import os
import traceback

from typing import Callable
from clparser.types.Command import Command
from clparser.errors.CommandErrors import DuplicateCommandError


class parser:
    # All the commands defined
    # are held in this dictionary
    __commands: dict

    def __init__(self,
                 name: str = "",
                 description: str = "Simple parser made with clparser.",
                 version: str = "v0.1.0") -> None:

        # Set the name of the parser
        self.__name = name if name != "" else os.path.basename(traceback.extract_stack()[-2].filename)[:-3]

        self.__description = description

        self.__version = version

        self.__commands = {
            "help": Command(
                name="help",
                desc="Shows this message.",
                usage=f"{self.__name} help",
                action=self.__print_help
            )
        }

    def add_command(self,
                    name: str, desc: str, usage: str, param_list: list[str] = None, action: Callable = None) -> bool:
        """

        Creating a command for the parser to execute.

        Examples on how to use this command are listed inside examples folder.

        :param name: name of the command
        :param desc: description of the command, used in help method
        :param usage: how the command is meant to be used, used in help method
        :param param_list: the list of the parameters the action needs, eg ["file", "dest"]. Defaults to None
        :param action: the callable action that the command executes. Takes in the params given in param_list.
                       Defaults to None
        :return: True if the command was created. False if the command wasn't.
        """
        try:

            if param_list is None:
                param_list = []

            if name in self.__commands.keys() and not (name == "help"):
                raise DuplicateCommandError("Please ensure you are not creating a duplicate command!")

            self.__commands[name] = Command(name=name,
                                            desc=desc,
                                            usage=usage,
                                            args=param_list,
                                            action=action)

            print(self.__commands.keys())
            return True

        except DuplicateCommandError:
            print("DuplicateCommandError: Overwriting the same command is forbidden aside from help.")
            return False

    @staticmethod
    def __parser_arguments(num_args, args) -> None | list[str]:
        """
        Determines the parameters needed by an action.

        :param num_args: the number of parameters needed
        :param args: the command line parameters.
        :return: The parameters given by the user or None
        """
        arguments: list = []

        if num_args == 0:
            return []

        if len(args) < num_args:
            return None

        for i in range(0, num_args):
            arguments.append(args[i])

        return arguments

    def __print_help(self) -> None:
        """
        boilerplate code for help function
        :return: None
        """

        cmds = ""
        for command_name, d in self.__commands.items():
            cmds += "\t" + command_name + "\t\t" + d.description + "\n"

        print(f"""
{self.__name} <command> 
\n\nPossible commands:\n{cmds}\n\n
{self.__name}@{self.__version}\n{self.__description}
            """)

    def parser(self, args: list) -> None:
        """
        Main part of the program.

        All the parsing is done inside this function.
        :param args: the command line parameters to parser through
        :return: None
        """

        # Making sure only the arguments
        # are passed through
        if args[0][-2:] == 'py':
            args = args[1:]

        if len(args) == 0 or 'help' in args:
            self.__print_help()
            return

        try:
            # Assuming the first argument
            # is a command
            command = self.__commands[args[0]]

            # Ensure arguments condition is met
            args_provided = self.__parser_arguments(command.param_len, args[1:])
            if args_provided is None and command.param_len > 0:
                print(f"Error: Expected {command.param_len} Arguments but none were given.")
                print("Use '" + self.__name + f" help {command.name}' to find how many arguments are needed!")

            command.run(*args_provided)

        except KeyError:
            print("Unknown command")
