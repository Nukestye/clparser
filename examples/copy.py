import sys
import shutil

from clparser.parser import Parser

from clparser.types.CommandActionParam import CommandActionParam
from clparser.types.FlagActionType import FlagActionType

def copy_func(cap: CommandActionParam):
    # Copy the file from one location to another
    # NOTE: Error handling needed
    shutil.copy(cap.file, cap.dest)
    
    if cap.containsFlag('--show') or cap.containsFlag('-s'):
        print(f"{cap.file} copied to {cap.dest}")


if __name__ == "__main__":
    p = Parser(
        "copy",
        "Copies a file",
        "v.3.0"
    )

    # Adding the command to the
    # Parser
    command = p.add_command(
        "copy",
        "Copies file from one place to another",
        "copy [file] [dest]",
        ["file", "dest"],
        copy_func,
    )
    
    # Adding a flag to the command
    command.add_flag(
        "show",
        "Shows a message at the end",
        ('-s', "--show"),
        FlagActionType.BOOL
    )

    # Executing the Parser
    p.parser(sys.argv)
