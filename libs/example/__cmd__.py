import libs.command as command

import argparse
import typing

class ExampleCommand(command.Command):
    """An example command
    """

    def __init__(self) -> None:
        """Creates an example command

        :param self:
            Self

        :return none:
        """

        super().__init__(name = "example")

    def addArguments(self, parser: argparse.ArgumentParser) -> None:
        """Adds our command's arguments

        :param self:
            Self
        :param parser:
            The parser to add our arguments to

        :return none:
        """

        parser.add_argument(
            "-t", "--test",
            required = True,
            help = "A test argument"
        )

    def runCommand(self, args: typing.List[object]) -> int:
        """Runs our command

        :param self:
            Self
        :param args:
            Our arguments

        :return int:
            Our result
        """

        self.io.print(f"Got argument value '{args.test}'")

        return 0
