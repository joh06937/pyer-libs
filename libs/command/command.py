import libs.util as util

import argparse
import inspect
import logging
import textwrap
import typing

class Command:
    """A light wrapper for argparse commands that tries to reduce a bit of the
    duck typing and feature set to keep it basic and a bit more structured
    """

    def __init__(
        self,
        name: str,
        help: str = None,
        description: str = None,
        subCommands: typing.List["Command"] = None
    ) -> None:
        """Creates a command

        If no help information is given for this command, this constructor will
        attempt to auto-generate both the short-form help text and the long-form
        description using the child class' docstring text.

        :param self:
            Self
        :param name:
            The name of this command (i.e. how it's invoked)
        :param help:
            Short-form information about this command
        :param description:
            Long-form information about this command
        :param subCommands:
            Sub-commands underneath this command

        :return none:
        """

        # If there is no help text, try to use the class' docstring
        if (help is None) or (description is None):
            lines = []

            # Go through the docstring line by line
            for line in self.__doc__.split("\n"):
                # Clear away and line endings and whitespace
                #
                # Docstrings will keep any whitespace for multi-line strings
                # that are spaced into a line. That is, this:
                #
                #     """This is some text
                #     This is some more
                #     """
                #
                # will result in "This is some more" having leading whitespace.
                line = line.strip()

                # If this is a blank line
                if len(line) < 1:
                    # If we don't have any text yet, they must just have some
                    # blank lines at the beginning of the docstring (like a
                    # lunatic), so trim these blank lines out
                    if len(lines) < 1:
                        continue

                # Add this line to our collection of lines
                lines.append(line)

            paragraphs = []
            paragraphStart = 0
            blankLineCount = 0

            # Piece together the paragraphs for each part of the docstring
            for i in range(len(lines)):
                # If this is a blank line
                if len(lines[i]) < 1:
                    # If we have a paragraph underway, this is the end of it
                    if paragraphStart is not None:
                        # Note the paragraph
                        paragraphs.append(lines[paragraphStart:i])

                        # Restart our search
                        paragraphStart = None

                        # Make sure we also keep this blank line
                        blankLineCount = 1

                    # Else, we have another blank line that we'll want to
                    # retain, but we can't use it during our justification
                    # operation, so note it separately
                    else:
                        blankLineCount += 1

                # Else, if we haven't started a paragraph yet
                elif paragraphStart is None:
                    # If we have blank lines we've been retaining
                    if blankLineCount > 0:
                        # Add those
                        [paragraphs.append([]) for blankLine in range(blankLineCount)]

                        # Restart our blank line counting
                        blankLineCount = 0

                    # Note the start of the paragraph
                    paragraphStart = i

                # Else, this is just another line in the paragraph, so nothing
                # to do

            # If there were lines at the end that didn't have a newline after
            # them, make sure we don't drop those
            if paragraphStart is not None:
                paragraphs.append(lines[paragraphStart:])

            descriptionParagraphs = []

            # Justify all of the paragraphs
            for paragraph in paragraphs:
                # If this is a blank line
                if len(paragraph) < 1:
                    # Add a space
                    #
                    # This is unfortunately the only way to get the output to
                    # preserve multiple blank lines in a row, which is what we'd
                    # prefer to do, since someone clearly went through the
                    # trouble of doing so in their docstring and thus must have
                    # some reason for them.
                    descriptionParagraphs.append(" ")
                else:
                    # Add the justified paragraph
                    descriptionParagraphs.append("\n".join(self._justifyLines(lines = paragraph, columns = 80)))

            # If there wasn't help text manually specified in our constructor,
            # use ours
            if help is None:
                help = descriptionParagraphs[0]

            # If there wasn't a description manually specified in our
            # constructor, use ours
            if description is None:
                description = "\n".join(descriptionParagraphs)

        if subCommands is None:
            subCommands = []

        self._name = name
        self._help = help
        self._description = description

        self._subCommands = subCommands

        # Python loggers should typically be gotten using:
        #
        #    logger = logging.getLogger(__name__)
        #
        # For the commands we're a base class of, that would be their
        # package/module location, so get that using the inspect library.
        moduleLocation = inspect.getmodule(self.__class__).__name__

        # All commands get a logger by default
        self.logger = logging.getLogger(moduleLocation)

        # All commands get output
        self.io = util.Terminal()

        # Note the location of this command's module so that all of its
        # package's loggers can get verbosity applied by our root command (when
        # we get to that point during run())
        self._logModules = [moduleLocation.split(".")[0]]

        # Also add all of our sub-commands' log modules so that the full command
        # structure's log modules all get bubbled up to the root one
        #
        # This isn't the most efficient way to do this -- we could probably
        # adjust a class variable or something -- but it's strings and this is
        # Python (and we're already grabbing the module names for other reasons)
        # so it's not really all that impactful.
        for subCommand in self._subCommands:
            self._logModules = list(set(self._logModules + subCommand._logModules))

    def _justifyLines(self, lines: typing.List[str], columns: int) -> typing.List[str]:
        """Justifies lines of text to a column width

        This assumes there are no blank lines in the list.

        :param self:
            Self
        :param lines:
            The lines to justify
        :param columns:
            What to justify the lines to

        :return typing.List[str]:
            The justified lines
        """

        # First make a single-line string out of the lines
        string = " ".join(lines)

        # Justify the text
        return textwrap.wrap(string, 80)

    def addArguments(self, parser: argparse.ArgumentParser) -> None:
        """Adds this command's arguments to the argument parser

        :param self:
            Self
        :param parser:
            The argument parser

        :return none:
        """

        pass

    def runCommand(self, args: typing.List[object]) -> typing.Union[None, int]:
        """Runs this command

        :param self:
            Self
        :param args:
            Arguments for the command

        :return None:
            Command not handled
        :return int:
            The result of running the command
        """

        return None

    def _addArguments(self, parser: argparse.ArgumentParser) -> None:
        """Adds this command's arguments to the argument parser

        :param self:
            Self
        :param parser:
            The argument parser

        :return none:
        """

        # Add our own arguments
        self.addArguments(parser = parser)

        # If we don't have any sub-commands, we're done
        if len(self._subCommands) < 1:
            return

        # Make a sub-parser list to add our sub-parsers to, and store the name
        # of the chosen sub-command (in the invocation) in a variable of our
        # choosing
        #
        # Note that we'll use the 'metavar' field to keep the output text from
        # listing all of the sub-commands in a giant list like:
        #
        #    Available sub-commands:
        #        {foo1,foo2,foo3,foo4,foo5}
        #            foo1        Foo 1
        #            foo2        Foo 2
        #            ...
        #
        # Since we're doing the help text for each sub-command in the list,
        # there's no reason to also have the bracketed single-line (wrapped)
        # text as well. It gets to be especially ugly when the line does indeed
        # need to wrap.
        #
        # Setting 'metavar' technically means there will be a blank line there
        # (the empty string). If someone wanted there to be some kind of custom
        # text for that, using 'metavar' and 'help' will create something like:
        #
        #    Available sub-commands:
        #        bar                Bar
        #            foo1        Foo 1
        #            foo2        Foo 2
        #            ...
        subParsers = parser.add_subparsers(
            title = "Available sub-commands",
            dest = f"_{self._name}SubCommandName",
            metavar = ""
        )

        # Add all of our sub-commands' arguments
        for subCommand in self._subCommands:
            # Make a sub-parser for this sub-command
            subParser = subParsers.add_parser(
                name = subCommand._name,
                help = subCommand._help,
                description = subCommand._description,
                formatter_class = argparse.RawTextHelpFormatter
            )

            # Add its arguments
            subCommand._addArguments(parser = subParser)

    def _runCommand(self, args: typing.List[object]) -> int:
        """Runs this command

        :param self:
            Self
        :param args:
            Arguments for the command

        :return int:
            The result of running the command
        """

        self.logger.debug(f"Letting this command ('{self._name}') have a go")

        # Always give ourselves the chance to handle this command
        result = self.runCommand(args = args)

        # If we handled it, use that as our result
        if result is not None:
            self.logger.debug(f"Command handled ({result})")
            return result

        # If this command doesn't have sub-commands available, er, nobody
        # handled it, apparently
        #
        # This could be an error, or it could just be a careless command that
        # didn't return a result, so just call this a success.
        if len(self._subCommands) < 1:
            self.logger.debug("Command not handled ourselves, and no sub-commands available")
            return 0

        # Get the sub-command of this command that was invoked, if any
        subCommandName = getattr(args, f"_{self._name}SubCommandName")

        # If there wasn't an invoked sub-command, er, nobody handled it,
        # apparently
        if (subCommandName is None) or (subCommandName == ""):
            self.logger.error("Please select one of the available sub-commands")
            return -1

        self.logger.debug(f"Sub-command '{subCommandName}' invoked, finding it...")

        # Find the command to run
        for subCommand in self._subCommands:
            # If this command wasn't the one invoked, keep looking
            if subCommand._name != subCommandName:
                continue

            self.logger.debug("Found sub-command")

            # This was the invoked command, so run it and use its result as ours
            return subCommand._runCommand(args = args)

        # We didn't find the matching command (somehow, since argparse is
        # supposed to handle that), so return an error
        self.logger.error(f"Couldn't find sub-command")
        return -1

    def run(self, args: typing.List[object] = None) -> int:
        """Runs the command as the root-most command

        :param self:
            Self
        :param args:
            Arguments for the command

        :return int:
            Our result
        """

        # Make a root parser for everything to flow from
        #
        # Note that we're setting the program name manually so it shows up as
        # something other than the root script file.
        rootParser = argparse.ArgumentParser(
            prog = self._name,
            description = self._description,
            formatter_class = argparse.RawTextHelpFormatter
        )

        # Add a verbosity argument, which will be global for all commands
        rootParser.add_argument(
            "-v", "--verbose",
            action = "count",
            default = 0,
            help = "Enable verbose logging (0: critical, 1: error, 2: warning, 3: info, 4: debug, 5: all modules debug)"
        )

        # Also add a logger argument to go along with the verbosity one
        rootParser.add_argument(
            "--logger",
            action = "append",
            default = [],
            help = "Specify the loggers to set up logging for (can specify multiple times)"
        )

        # Add our and our sub-commands' arguments, recursively
        self._addArguments(parser = rootParser)

        # Parse the provided arguments
        args = rootParser.parse_args(args = args)

        # The verbosity is global, so handle that, regardless of which command
        # was invoked
        #
        # If there weren't any loggers specified
        if len(args.logger) < 1:
            # Get the package that Command is under
            ourModule = inspect.getmodule(Command).__name__.split(".")[0]

            # Get loggers for our module and all of the log modules we found for
            # our commands
            args.logger = list(set([ourModule] + self._logModules))

        # If they specified enough verbosity, get the root logger (meaning *all*
        # modules will have their loggers enabled)
        if args.verbose >= 5:
            args.logger = [logging.getLogger()]
        # Else, get the command loggers
        else:
            args.logger = [logging.getLogger(logger) for logger in args.logger]

        for logger in args.logger:
            # Set the appropriate logging level
            if args.verbose >= 4:
                logger.setLevel(logging.DEBUG)
            elif args.verbose >= 3:
                logger.setLevel(logging.INFO)
            elif args.verbose >= 2:
                logger.setLevel(logging.WARNING)
            elif args.verbose >= 1:
                logger.setLevel(logging.ERROR)
            else:
                logger.setLevel(logging.CRITICAL)

            handler = logging.StreamHandler()
            logger.addHandler(handler)

        # Try to run the command, recursively
        try:
            result = self._runCommand(args = args)

        # If the user stops the command, don't bother letting the exception rise
        # all the way up to the terminal, just do a quiet exit
        except KeyboardInterrupt:
            self.io.print("^C")

            return 1

        # Remove all of the logging handlers we created, just in case we're run
        # again without this Python instance getting destroyed
        for logger in args.logger:
            logger.removeHandler(logger.handlers[0])

        return result
