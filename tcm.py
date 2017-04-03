"""This module provides a framework for generating test methods at runtime."""


ATTR_NAME = 'tcm values'


class DecoratorException(Exception):
    """Exception raised on invalid use of the "values" decorator."""

    pass


def values(*args, **kwargs):
    """Create a parameterized decorator which stores its arguments in the decorated object."""
    if len(args) == 1 and callable(args[0]) and not kwargs:
        raise DecoratorException(
            'Invalid use without parentheses or with a callable as the only argument')

    def _decorator(func):
        setattr(func, ATTR_NAME, (args, kwargs))
        return func

    return _decorator
