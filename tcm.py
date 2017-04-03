"""This module provides a framework for generating test methods at runtime."""


ATTR_NAME = 'tcm values'


def values(*args, **kwargs):
    """Create a parameterized decorator which stores its arguments in the decorated object."""
    def _decorator(func):
        setattr(func, ATTR_NAME, (args, kwargs))
        return func

    return _decorator
