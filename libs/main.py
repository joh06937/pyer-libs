import libs.command as command

import typing

def main(args: typing.List[object] = None) -> int:
    """Main

    :param args:
        Our arguments

    :return int:
        Our result
    """

    rootCommand = command.Command(
        name = "root",
        help = "The root command",
        subCommands = [
        ]
    )

    # Run the root command and return its result
    return rootCommand.run()
