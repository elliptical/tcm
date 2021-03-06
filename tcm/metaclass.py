"""This module provides a metaclass for generating test methods at runtime."""


from collections import OrderedDict
import functools
import inspect

from .decorator import extract_captured_arguments


class MetaclassException(Exception):
    """Exception raised on errors when generating test methods."""


class TestCaseMeta(type):
    """Metaclass based runtime generator of the test methods."""

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):  # pylint: disable=unused-argument
        """Use ordered mapping for the namespace regardless of the Python version."""
        # Note: absent the __prepare__() method, Python 3.6 would use an ordered
        # mapping while prior versions would stick with a regular dict().
        return OrderedDict()

    def __new__(cls, name, bases, mapping):
        """Create the class after expanding the original mapping."""
        new_mapping = dict()
        for key, value in _expanded_mapping(mapping):
            if key in new_mapping:
                existing = _get_starting_line_number(new_mapping[key])
                current = _get_starting_line_number(value)
                raise MetaclassException(
                    f'Duplicate "{key}" attribute at lines {existing} and {current}')
            new_mapping[key] = value
        return super().__new__(cls, name, bases, new_mapping)


def _expanded_mapping(mapping):
    """Iterate the mapping while generating new test methods from decorated ones."""
    for key, value in mapping.items():
        try:
            captured_arguments = extract_captured_arguments(value)
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
        raise MetaclassException(f'Invalid test arg: {arg!r}')

    functools.update_wrapper(_wrapper, func)

    return _wrapper


def _get_starting_line_number(func):
    """Return the starting line number of the test method definition."""
    _, start_line_number = inspect.getsourcelines(func)
    return start_line_number
