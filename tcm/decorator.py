"""This module provides a decorator to capture test method inputs."""


from collections import namedtuple


ATTR_NAME = 'tcm values'
TEST_METHOD_PREFIX = 'test'


class DecoratorException(Exception):
    """Exception raised on invalid use of the "values" decorator."""


class values():  # noqa: N801 / pylint: disable=invalid-name,too-few-public-methods
    """Parameterized decorator which stores its arguments in the decorated object."""

    def __init__(self, *args, **kwargs):
        """Capture the decorator arguments."""
        if len(args) == 1 and callable(args[0]) and not kwargs:
            raise DecoratorException(
                'Invalid use without parentheses or with a callable as the only argument')
        self.__captured_arguments = _CapturedArguments(args, kwargs)

    def __call__(self, func):
        """Store the captured arguments in the decorated object."""
        if not callable(func):
            raise DecoratorException('The object must be callable')
        if not func.__name__.startswith(TEST_METHOD_PREFIX):
            raise DecoratorException(
                'The object name must start with "{}"'.format(TEST_METHOD_PREFIX))

        try:
            attr = getattr(func, ATTR_NAME)
        except AttributeError:
            setattr(func, ATTR_NAME, self.__captured_arguments)
        else:
            if isinstance(attr, _CapturedArguments):
                raise DecoratorException('Cannot decorate the same object more than once')
            else:
                raise DecoratorException(
                    'The object already has the "{}" attribute'.format(ATTR_NAME))

        return func


def extract_captured_arguments(func):
    """Raise AttributeError for non-decorated "func", return the captured arguments otherwise."""
    captured_arguments = getattr(func, ATTR_NAME)
    if type(captured_arguments) is not _CapturedArguments:  # pylint: disable=unidiomatic-typecheck
        # The attribute was not set by tcm, so effectively it does not exist.
        raise AttributeError
    delattr(func, ATTR_NAME)
    return captured_arguments


_CapturedArguments = namedtuple('CapturedArguments', 'args, kwargs')
