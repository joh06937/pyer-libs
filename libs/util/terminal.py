class Terminal:
    """A wrapper for terminal IO
    """

    def print(self, *args, **kwargs) -> None:
        """Prints a string

        :param self:
            Self
        :param *args:
            Positional arguments for print()
        :param **kwargs:
            Keyword arguments for print()

        :return none:
        """

        print(*args, **kwargs, flush = True)

    def _printVt100(self, code: str) -> None:
        """Prints a VT100 code

        :param self:
            Self
        :param code:
            The code to print

        :return none:
        """

        self.print(f"\033{code}", end = "")

    def success(self, *args, **kwargs) -> None:
        """Prints a success string

        :param self:
            Self
        :param *args:
            Positional arguments for print()
        :param **kwargs:
            Keyword arguments for print()

        :return none:
        """

        self._printVt100(code = "[32m")
        self.print(*args, **kwargs)
        self._printVt100(code = "[0m")

    def error(self, *args, **kwargs) -> None:
        """Prints an error string

        :param self:
            Self
        :param *args:
            Positional arguments for print()
        :param **kwargs:
            Keyword arguments for print()

        :return none:
        """

        self._printVt100(code = "[31m")
        self.print(*args, **kwargs)
        self._printVt100(code = "[0m")

    def warning(self, *args, **kwargs) -> None:
        """Prints a warning string

        :param self:
            Self
        :param *args:
            Positional arguments for print()
        :param **kwargs:
            Keyword arguments for print()

        :return none:
        """

        self._printVt100(code = "[33m")
        self.print(*args, **kwargs)
        self._printVt100(code = "[0m")

    def reprint(self, *args, **kwargs) -> None:
        """Reprints a string to the current line

        :param self:
            Self
        :param *args:
            Positional arguments for print()
        :param **kwargs:
            Keyword arguments for print()

        :return none:
        """

        self.clearLine()
        self.print(*args, **kwargs)

    def topLeft(self) -> None:
        """Moves the cursor to the top-left corner

        :param self:
            Self

        :return none:
        """

        self._printVt100("[H")

    def clearScreen(self) -> None:
        """Clears the screen

        :param self:
            Self

        :return none:
        """

        self._printVt100("[2J")

    def clearLine(self) -> None:
        """Clears the current line

        :param self:
            Self

        :return none:
        """

        self._printVt100("[2K\r")

    def upLines(self, lineCount: int) -> None:
        """Moves the cursor up lines

        :param self:
            Self
        :param lineCount:
            How many lines to go up

        :return none:
        """

        self._printVt100(f"[{lineCount}A")

    def getInput(self, prompt: str = None) -> str:
        """Gets input

        :param self:
            Self
        :param prompt:
            A prompt to print

        :return str:
            Input
        """

        if prompt is not None:
            self.print(prompt)

        self.print("[Enter]: ", end = "")

        return input()
