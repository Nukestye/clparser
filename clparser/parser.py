import os
import traceback

from typing import Callable
from clparser.types.Command import Command
from clparser.errors.CommandErrors import DuplicateCommandError


class parser:
    # All the commands defined
    # are held in this dictionary
    __commands: dict
    __flags: dict

    def __init__(
        self,
        name: str = "",
        description: str = "Simple parser made with clparser.",
        version: str = "v0.1.0",
    ) -> None:
        # Set the name of the parser
        self.__name = (
            name
            if name != ""
            else os.path.basename(traceback.extract_stack()[-2].filename)[:-3]
        )

        self.__description = description

        self.__version = version

        self.__commands = {
            "help": Command(
                name="help",
                desc="Shows this message.",
                usage=f"{self.__name} help",
                action=self.__print_help,
            )
        }

    def add_flag(self, flag_notation: str, command: Command | str = "global") -> None:
        """
        Add flag to the command

        :param str flag_notation: the notation used by the user in command line
        :param Command | str command: The command the flag is linked to,
        takes either Command or str. Defaults to "global"
        """
        pass

    def add_command(
        self,
        name: str,
        desc: str,
        usage: str,
        param_list: list[str] = None,
        action: Callable = None,
    ) -> bool:
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
                raise DuplicateCommandError(
                    "Please ensure you are not creating a duplicate command!"
                )

            self.__commands[name] = Command(
                name=name, desc=desc, usage=usage, args=param_list, action=action
            )

            return True

        except DuplicateCommandError:
            print(
                "DuplicateCommandError: Overwriting the same command is forbidden aside from help."
            )
            return False

    def __find_params(
        self, args: list[any], num_args_needed: int
    ) -> list[list[str], list[str]]:
        """
        Finds the params and flags from the arguemnts provided in the command line.


        :param list[str] args: the arguments given from the command line
        :param int num_args_needed: The number of params the action function needs

        :returns  list[list[str], list[str]]: The params in index 0 and flags in index 1 found in arguments given
        """
        arguments_found: list[str] = []
        flags_found: list[str] = []
        # Iterator i
        i: int = 0

        if len(args) < num_args_needed:
            return None

        while len(arguments_found) != num_args_needed:
            # No arguments were provided
            if i == len(args):
                break

            # Making the line length shorter
            param = args[i]
            if param.startswith("-") or param.startswith("--"):
                flags_found.append(param)
                i += 1
                continue

            arguments_found.append(param)
            i += 1
            continue

        for j in range(i, len(args)):
            param = args[j]
            if param.startswith("-") or param.startswith("--"):
                flags_found.append(param)

        return [arguments_found, flags_found]

    def __print_help(self) -> None:
        """
        boilerplate code for help function
        :return: None
        """

        cmds = ""
        for command_name, d in self.__commands.items():
            cmds += "\t" + command_name + "\t\t" + d.description + "\n"

        print(
            f"""
{self.__name} <command> 
\n\nPossible commands:\n{cmds}\n\n
{self.__name}@{self.__version}\n{self.__description}
            """
        )

    def parser(self, args: list) -> None:
        """
        Main part of the program.

        All the parsing is done inside this function.
        :param args: the command line parameters to parser through
        :return: None
        """

        # Making sure only the arguments
        # are passed through
        if args[0][-2:] == "py":
            args = args[1:]

        if len(args) == 0 or "help" in args:
            self.__print_help()
            return

        # TODO: Check if the cl program is commandless.
        # see note 'commandless' for specifics

        try:
            # [commandless] NOTE: Parser by default assumes that the first argument given
            # in the command line, is a command. Which can prevent commandless
            # programs from working. i.e. 'copy [file] [dest]' won't work but
            # 'copy copy [file] [dest]' will work.
            command = self.__commands[args[0]]

            # Ensure arguments condition is met
            args_found = self.__find_params(args[1:], command.param_len)
            if args_found is None and command.param_len > 0:
                print(
                    f"Error: Expected {command.param_len} Arguments but none were given."
                )
                print(
                    f"Use '{self.__name} help {command.name}' to find how many arguments are needed!"
                )

            command.run(*args_found)

        except KeyError:
            print("Unknown command")
