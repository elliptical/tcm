"""This module provides a framework for generating test methods at runtime."""


ATTR_NAME = 'tcm values'
TEST_METHOD_PREFIX = 'test'


class DecoratorException(Exception):
    """Exception raised on invalid use of the "values" decorator."""

    pass


class values():  # noqa: N801 / pylint: disable=invalid-name,too-few-public-methods
    """Parameterized decorator which stores its arguments in the decorated object."""

    def __init__(self, *args, **kwargs):
        """Capture the decorator arguments."""
        if len(args) == 1 and callable(args[0]) and not kwargs:
            raise DecoratorException(
                'Invalid use without parentheses or with a callable as the only argument')
        self.__captured_arguments = (args, kwargs)

    def __call__(self, func):
        """Store the captured arguments in the decorated object."""
        if not callable(func):
            raise DecoratorException('The object must be callable')
        if not func.__name__.startswith(TEST_METHOD_PREFIX):
            raise DecoratorException(
                'The object name must start with "{}"'.format(TEST_METHOD_PREFIX))
        setattr(func, ATTR_NAME, self.__captured_arguments)
        return func
