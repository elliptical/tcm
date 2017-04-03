import unittest

import tcm


class DecoratorTestCase(unittest.TestCase):
    def test_missing_arguments_are_stored(self):
        @tcm.values()
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {})

    def test_single_positional_argument_is_stored(self):
        @tcm.values('abc')
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ('abc',))
        self.assertDictEqual(kwargs, {})

    def test_single_keyword_argument_is_stored(self):
        @tcm.values(kw=None)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {'kw': None})

    def test_mixed_arguments_are_stored(self):
        @tcm.values('abc', 12, kw=None)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ('abc', 12))
        self.assertDictEqual(kwargs, {'kw': None})
