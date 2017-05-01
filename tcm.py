"""This module provides a framework for generating test methods at runtime."""


from collections import namedtuple
from collections import OrderedDict
import functools
import inspect


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


class MetaclassException(Exception):
    """Exception raised on errors when generating test methods."""

    pass


class TestCaseMeta(type):
    """Metaclass based runtime generator of the test methods."""

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):  # noqa: N804 pylint: disable=unused-argument
        """Use ordered mapping for the namespace regardless of the Python version."""
        # Note: absent the __prepare__() method, Python 3.6 would use an ordered
        # mapping while prior versions would stick with a regular dict().
        return OrderedDict()

    def __new__(mcs, name, bases, mapping):  # noqa: N804
        """Create the class after expanding the original mapping."""
        new_mapping = dict()
        for key, value in _expanded_mapping(mapping):
            if key in new_mapping:
                existing = _get_starting_line_number(new_mapping[key])
                current = _get_starting_line_number(value)
                raise MetaclassException(
                    'Duplicate "{}" attribute at lines {} and {}'.format(key, existing, current))
            new_mapping[key] = value
        return super().__new__(mcs, name, bases, new_mapping)


def _expanded_mapping(mapping):
    """Iterate the mapping while generating new test methods from decorated ones."""
    for key, value in mapping.items():
        try:
            captured_arguments = _extract_captured_arguments(value)
        except AttributeError:
            # Pass non-decorated items unchanged.
            yield key, value
        else:
            # Use the decorated test method as a sample and generate a distinct
            # test method for every captured argument.
            as_is = _has_single_test_param(value)
            for suffix, arg in _uniformly_named_arguments(captured_arguments):
                generated = _generate_test_method(value, arg, as_is)
                generated.__name__ = key + '_' + suffix
                yield generated.__name__, generated


def _extract_captured_arguments(func):
    """Raise AttributeError for non-decorated "func", return the captured arguments otherwise."""
    captured_arguments = getattr(func, ATTR_NAME)
    if type(captured_arguments) is not _CapturedArguments:  # pylint: disable=unidiomatic-typecheck
        # The attribute was not set by tcm, so effectively it does not exist.
        raise AttributeError
    delattr(func, ATTR_NAME)
    return captured_arguments


def _has_single_test_param(func):
    sig = inspect.signature(func)
    params = sig.parameters
    if len(params) != 2:
        return False
    _, test_param = params.values()
    return test_param.kind == test_param.POSITIONAL_OR_KEYWORD


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


def _generate_test_method(func, arg, as_is):
    """Wrap the original test method by supplying the (possibly unpacked) "arg"."""
    if as_is:
        def _wrapper(self):
            return func(self, arg)
    elif isinstance(arg, (tuple, list)):
        def _wrapper(self):
            return func(self, *arg)
    elif isinstance(arg, dict):
        def _wrapper(self):
            return func(self, **arg)
    else:
        raise MetaclassException('Invalid test arg: {!r}'.format(arg))

    functools.update_wrapper(_wrapper, func)

    return _wrapper


def _get_starting_line_number(func):
    """Return the starting line number of the test method definition."""
    # Python 3.4 version of getsourcelines() will return the source of the
    # wrapper instead of the wrapped, so we unwrap it first (this is what
    # Python 3.5 and higher do).
    func = inspect.unwrap(func)
    _, start_line_number = inspect.getsourcelines(func)
    return start_line_number
