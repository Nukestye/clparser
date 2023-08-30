
import os
import traceback

from typing import Callable
from clparser.types.Command import Command, ActionParam


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
                    name: str,
                    desc: str,
                    usage: str,
                    param_list: list[str] = [],
                    action: Callable = None) -> bool:
        try:
           
           self.__commands[name] = Command(name=name,
                                           desc=desc,
                                           usage=usage,
                                           args=param_list,
                                           action=action)
           
           print(f"'{name}' command created")
           return True
            
        except ValueError:
            print("Unknown problem, please ensure you are not creating a duplicate command")
            return False
    
    
    @staticmethod
    def __parser_arguments(num_args, args):

        arguments: list = []

        if num_args == 0:
            return []

        if len(args) < num_args:
            return None

        for i in range(0, num_args):
            arguments.append(args[i])

        return arguments
    
    def __print_help(self, ap: ActionParam):

        cmds = ""
        for command_name, d in self.__commands.items():
            cmds += "\t" + command_name + "\t\t" + d.description + "\n"

        print(f"""
{self.__name} <command> 
\n\nPossible commands:\n{cmds}\n\n
{self.__name}@{self.__version}\n{self.__description}
            """)
    
    def parser(self, args: list) -> None:
        
        # Making sure only the arguments
        # are passed through
        if args[0][-2:] == 'py':
            args = args[1:]
        
        if len(args) == 0:
            self.__print_help()
            return
        
        try:
            # Assuming the first argument
            # is a command
            command = self.__commands[args[0]]
            
            # Ensure arguments condition is met
            args = self.__parser_arguments(command.param_len, args[1:])
            
            if args is None and command.param_len > 0:
                print(f"Error: Expected {command.param_len} Arguments but none were given.")
                print("Use '" + self.__name + f" help {args[0]}' to find how many arguments are needed!")
            
            command.run(*args)
            
        except KeyError:
            print("Unknown command")
