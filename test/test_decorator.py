import unittest

import tcm
from tcm.decorator import ATTR_NAME


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

        self.assertIsInstance(test, tcm.values)

    def test_missing_arguments_are_stored(self):
        @tcm.values()
        def test():
            pass  # pragma: no cover

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {})

    def test_single_positional_noncallable_argument_is_stored(self):
        @tcm.values('abc')
        def test():
            pass  # pragma: no cover

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
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

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
        self.assertTupleEqual(args, (_dummy_callable, 12))
        self.assertDictEqual(kwargs, {})

    def test_callable_argument_with_a_keyword_argument_are_stored(self):
        @tcm.values(_dummy_callable, kw=None)
        def test():
            pass  # pragma: no cover

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
        self.assertTupleEqual(args, (_dummy_callable,))
        self.assertDictEqual(kwargs, {'kw': None})

    def test_single_keyword_noncallable_argument_is_stored(self):
        @tcm.values(kw=None)
        def test():
            pass  # pragma: no cover

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {'kw': None})

    def test_single_keyword_callable_argument_is_stored(self):
        @tcm.values(kw=_dummy_callable)
        def test():
            pass  # pragma: no cover

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
        self.assertTupleEqual(args, ())
        self.assertDictEqual(kwargs, {'kw': _dummy_callable})

    def test_mixed_arguments_are_stored(self):
        @tcm.values('abc', 12, kw=None)
        def test():
            pass  # pragma: no cover

        self.assertNotIsInstance(test, tcm.values)
        args, kwargs = getattr(test, ATTR_NAME)
        self.assertTupleEqual(args, ('abc', 12))
        self.assertDictEqual(kwargs, {'kw': None})

    def test_noncallable_object_will_raise(self):
        with self.assertRaises(tcm.DecoratorException) as cm:
            @tcm.values()
            @_zilch
            def test():  # pylint: disable=unused-variable
                pass  # pragma: no cover

        self.assertEqual(cm.exception.args[0], 'The object must be callable')

    def test_unexpected_name_prefix_will_raise(self):
        with self.assertRaises(tcm.DecoratorException) as cm:
            @tcm.values()
            def func():  # pylint: disable=unused-variable
                pass  # pragma: no cover

        self.assertEqual(cm.exception.args[0], 'The object name must start with "test"')

    def test_multiple_decorators_will_raise(self):
        with self.assertRaises(tcm.DecoratorException) as cm:
            @tcm.values()
            @tcm.values()
            def test():  # pylint: disable=unused-variable
                pass  # pragma: no cover

        self.assertEqual(cm.exception.args[0], 'Cannot decorate the same object more than once')

    def test_already_existing_attribute_will_raise(self):
        def test():
            pass  # pragma: no cover

        setattr(test, ATTR_NAME, None)

        with self.assertRaises(tcm.DecoratorException) as cm:
            test = tcm.values()(test)

        self.assertEqual(cm.exception.args[0], 'The object already has the "tcm values" attribute')


def _zilch(_func):
    return None


def _dummy_callable():
    pass    # pragma: no cover
