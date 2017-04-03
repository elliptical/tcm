import unittest

import tcm


class DecoratorTestCase(unittest.TestCase):
    def test_missing_parentheses_will_normally_raise(self):
        with self.assertRaises(tcm.DecoratorException) as cm:
            @tcm.values
            def test():  # pylint: disable=unused-variable
                pass  # pragma: no cover

        self.assertEqual(
            cm.exception.args[0],
            'Invalid use without parentheses or with a callable as the only argument')

    def test_missing_parentheses_will_not_raise_for_determined_users(self):
        @tcm.values
        @_zilch
        def test():
            pass  # pragma: no cover

        self.assertFalse(hasattr(test, tcm.ATTR_NAME))
        self.assertEqual(test.__name__, '_decorator')

    def test_missing_arguments_are_stored(self):
        @tcm.values()
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {})

    def test_single_positional_noncallable_argument_is_stored(self):
        @tcm.values('abc')
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ('abc',))
        self.assertDictEqual(kwargs, {})

    def test_single_positional_callable_argument_will_raise(self):
        with self.assertRaises(tcm.DecoratorException) as cm:
            @tcm.values(_dummy_callable)
            def test():  # pylint: disable=unused-variable
                pass  # pragma: no cover

        self.assertEqual(
            cm.exception.args[0],
            'Invalid use without parentheses or with a callable as the only argument')

    def test_callable_argument_with_another_positional_argument_are_stored(self):
        @tcm.values(_dummy_callable, 12)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, (_dummy_callable, 12))
        self.assertDictEqual(kwargs, {})

    def test_callable_argument_with_a_keyword_argument_are_stored(self):
        @tcm.values(_dummy_callable, kw=None)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, (_dummy_callable,))
        self.assertDictEqual(kwargs, {'kw': None})

    def test_single_keyword_noncallable_argument_is_stored(self):
        @tcm.values(kw=None)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {'kw': None})

    def test_single_keyword_callable_argument_is_stored(self):
        @tcm.values(kw=_dummy_callable)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {'kw': _dummy_callable})

    def test_mixed_arguments_are_stored(self):
        @tcm.values('abc', 12, kw=None)
        def test():
            pass  # pragma: no cover

        args, kwargs = getattr(test, tcm.ATTR_NAME)
        self.assertTupleEqual(args, ('abc', 12))
        self.assertDictEqual(kwargs, {'kw': None})


def _zilch(dummy):
    return None


def _dummy_callable():
    pass    # pragma: no cover
