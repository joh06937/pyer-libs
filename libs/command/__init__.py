from .command import Command

import libs.util as util

import importlib
import importlib.metadata

__all__ = [
	"Command",
]

def run(entryPointsNamespace: str) -> int:
    """Runs our commands

    This helper will do two things:

    1) Gather all of the entry points registered as commands
    2) Create and run a root command using the arguments provided to the system

    Entry points can be registered by packages in their setup.cfg (or
    equivalent) like so:

    ```
    [entry_points]
    foo.bar =
        thing1 = thing.whatever:ClassName
    foo.bar =
        thing2 = blah.bloo:AnotherClassName
    ```

    Then the `entryPointsNamespace` parameter for this function should be
    `foo.bar`, letting our filtering below capture everything registered under
    that namespace. This will then import each module registered (e.g.
    `thing.whatever`), grab its specified class (e.g. `ClassName`), and
    instantiate said class as a sub-command to the auto-created root command.

    :param entryPointsNamespace:
        The namespace that the entry points are registered under

    :return int:
        Our result
    """

    # Make some IO to act like a command before we actually get a command made
    io = util.Terminal()

    # Get all of the entry points registered for this instance of Python
    entryPoints = importlib.metadata.entry_points()

    # Get only the entry points we care about
    entryPoints = [entryPoint for entryPoint in entryPoints if entryPoint.group == entryPointsNamespace]

    subCommands = []

    # For each entry point, try to make a class out of its designation
    for entryPoint in entryPoints:
        fields = entryPoint.value.split(":")

        # If we don't have the correct format, that's a paddlin'
        if len(fields) != 2:
            io.error(f"Entry point '{entryPoint}' has an invalid format (expect 'module:ClassName')")
            return -1

        # Try to import its module
        module = importlib.import_module(fields[0])

        # If the module doesn't have the specified class, that's a paddlin'
        if not hasattr(module, fields[1]):
            io.error(f"Entry point '{entryPoint}' class '{fields[1]}' not found")
            return -1

        # Get the command class from the module
        command = getattr(module, fields[1])

        # If that failed, that's a paddlin'
        if command is None:
            io.error(f"Entry point '{entryPoint}' class '{fields[1]}' not imported")
            return -1

        # Add the class as a sub-command
        subCommands.append(command())

    # Make a root command
    rootCommand = Command(
        name = "root",
        help = "The root command",
        description = "This command has been auto-generated.",
        subCommands = subCommands
    )

    # Run the root command and return its result
    return rootCommand.run()
