import re
from typing import Callable


class CommandMeta:
    name: str
    description: str
    usage: str

    def __init__(self, name: str, description: str, usage: str) -> None:
        self.name = name
        self.description = description
        self.usage = usage


class ActionParam:
    pass


class Command(CommandMeta):
    param: list[str]
    param_len: int  # len(param)

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

    def run(self, *args: tuple) -> bool:
        if len(args[0]) != self.param_len:
            print(f"Arguments given are {len(args[0])} but needed {self.param_len}")
            return False

        # Using the index of each argument
        # in param
        # define it inside ActionParam
        # then sent it in action function
        ap = ActionParam

        for index in range(self.param_len):
            var = self.param[0][index]

            regex = re.compile("[\W0-9]")

            # Check if the variable name is valid
            if regex.match(var):
                print("Unable to create a variable with numbers/special characters")
                return False

            setattr(ap, self.param[index], args[0][index])

        # NOTE: Flags are not processed
        # Regardless of the users intention to need arguments
        # in action function, the flags variable will be set by default
        # and cannot be changed
        setattr(ap, "flags", args[1])

        self.action(ap)

        return True
