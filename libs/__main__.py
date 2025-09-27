import sys
import typing

import libs.command as command

def main() -> None:
    """Main

    :param args:
        Our arguments

    :return none:
    """

    sys.exit(command.run(entryPointsNamespace = "pyer.commands"))

if __name__ == "__main__":
    main()
