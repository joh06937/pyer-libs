"""
Test
"""

@service
def erik_test(arg1: int, arg2: bool) -> str:
    """Runs Erik test

    :param arg1:
        Argument 1
    :param arg2:
        Argument 2

    :return str:
        Our result
    """

    log.info(f"Hello, this is Erik's test with arg1 '{arg1}' and arg2 '{arg2}'")

    if arg1 != 0:
        return "Zero"
    elif arg2:
        return "True"
    else:
        return "False"
