"""This package provides a framework for generating test methods at runtime."""


__version__ = '1.0.2'


import unittest

from .decorator import DecoratorException   # noqa: F401
from .decorator import values               # noqa: F401
from .metaclass import MetaclassException   # noqa: F401
from .metaclass import TestCaseMeta


class TestCase(unittest.TestCase, metaclass=TestCaseMeta):
    """Base class to automatically employ the TestCaseMeta metaclass."""
