"""This module provides a framework for generating test methods at runtime."""


from collections import namedtuple
import functools


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


_CapturedArguments = namedtuple('CapturedArguments', 'args, kwargs')


class TestCaseMeta(type):
    """Metaclass based runtime generator of the test methods."""

    def __new__(mcs, name, bases, mapping):  # noqa: N804
        """Create the class after expanding the original mapping."""
        new_mapping = dict(_expanded_mapping(mapping))
        return super().__new__(mcs, name, bases, new_mapping)


def _expanded_mapping(mapping):
    """Iterate the mapping while generating new test methods from decorated ones."""
    for key, value in mapping.items():
        try:
            captured_arguments = _get_captured_arguments(value)
        except AttributeError:
            # Pass non-decorated items unchanged.
            yield key, value
        else:
            # Use the decorated test method as a sample and generate a distinct
            # test method for every captured argument.
            for suffix, arg in _uniformly_named_arguments(captured_arguments):
                generated = _generate_test_method(value, arg)
                generated.__name__ = key + '_' + suffix
                yield generated.__name__, generated


def _get_captured_arguments(func):
    """Raise AttributeError for non-decorated "func", return the captured arguments otherwise."""
    captured_arguments = getattr(func, ATTR_NAME)
    if type(captured_arguments) is not _CapturedArguments:  # pylint: disable=unidiomatic-typecheck
        # The attribute was not set by tcm, so effectively it does not exist.
        raise AttributeError
    return captured_arguments


def _uniformly_named_arguments(captured_arguments):
    """Iterate the captured arguments as uniform name/value pairs."""
    args, kwargs = captured_arguments

    # For positional arguments, the name is 1-based index padded with
    # leading zeroes to the length of the last index.
    width = len(str(len(args)))
    for i, arg in enumerate(args, 1):
        name = str(i).zfill(width)
        yield name, arg

    # For keyword arguments, the keyword is taken as a name.
    yield from kwargs.items()


def _generate_test_method(func, arg):
    """Wrap the original test method by supplying the "arg" as a positional argument."""
    @functools.wraps(func)
    def _wrapper(self):
        return func(self, arg)

    return _wrapper
