import re
from typing import Callable

from clparser.types.Flag import Flag
from clparser.types.CommandActionParam import CommandActionParam
from clparser.types.FlagActionType import FlagActionType

class CommandMeta:
    name: str
    description: str
    usage: str

    def __init__(self, name: str, description: str, usage: str) -> None:
        self.name = name
        self.description = description
        self.usage = usage


class Command(CommandMeta):
    param: list[str]
    param_len: int  # len(param)
    
    flags: dict

    action: Callable | None
    

    def __init__(
        self,
        name: str,
        desc: str,
        usage: str,
        args: list[str] = [],
        action: Callable | None = None,
    ) -> None:
        super().__init__(name=name, description=desc, usage=usage)
        self.param = args
        self.param_len = len(args)
        self.action = action
        # keep-flag-hidden NOTE(nukestye): Make flags hidden to prevent them from
        # being overwritten directly, have a getter function for users who
        # wish to see the full list of flags for the command
        self.flags = {}


    def add_flag(
            self,
            name: str,
            desc: str,
            flag_notation: str | list,
            action: FlagActionType) -> None:
        """
        Add flag to the command

        :param name: the name of the flag
        :type name: str
        :param desc: info graphic used in help command
        :type desc: str
        :param flag_notation: the notation used by the user in command line
        :type flag_notation: str
        :param action: the type of action the flag needs to process
        :type action: FlagActionType
        """
        if name in self.flags:
            print("Flag cannot have the same name as another.")
            return

        flag = Flag(name, desc, flag_notation, action)

        self.flags[flag_notation] = flag

    def run(self, *args: tuple) -> bool:
        if len(args[0]) != self.param_len:
            print(f"Arguments given are {len(args[0])} but needed {self.param_len}")
            return False

        # Using the index of each argument
        # in param
        # define the params inside CommandActionParam
        # as varaibles using 'setattr'
        # then send them in the action function
        cap = CommandActionParam()

        for index in range(self.param_len):
            var = self.param[0][index]

            regex = re.compile("[\W0-9]")

            # Check if the variable name is valid
            if regex.match(var):
                print("Unable to create a variable with numbers/special characters")
                return False

            setattr(cap, self.param[index], args[0][index])

        # NOTE: Flags are not processed
        # Regardless of the users intention to need arguments
        # in action function, the flags variable will be set by default
        # and cannot be changed
        setattr(cap, "flags", args[1])

        self.action(cap)

        return True
