import sys
import shutil

from clparser.parser import parser

from clparser.types.Command import ActionParam


def copy_func(ap: ActionParam):
    # Copy the file from one location to another
    # NOTE: Error handling needed
    shutil.copy(ap.file, ap.dest)
    print(f"{ap.file} copied to {ap.dest}")


if __name__ == "__main__":
    p = parser("copy", "Copies a file", "v1.0.0")

    # Adding the command to the
    # Parser
    p.add_command(
        name="copy",
        desc="Copies file from one place to another",
        usage="copy [file] [dest]",
        param_list=["file", "dest"],
        action=copy_func,
    )

    # Executing the Parser
    p.parser(sys.argv)
