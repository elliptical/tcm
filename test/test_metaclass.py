import inspect
import unittest

import tcm
from tcm.decorator import ATTR_NAME


class MetaclassTestCase(unittest.TestCase):
    # pylint: disable=no-member

    def test_nondecorated_test_methods_keep_their_names(self):
        class GeneratedTestCase(tcm.TestCase):
            def test_no_attr(self):
                pass  # pragma: no cover

            def test_user_attr(self):
                pass  # pragma: no cover

            setattr(test_user_attr, ATTR_NAME, None)

        self.assertFalse(hasattr(GeneratedTestCase.test_no_attr, ATTR_NAME))
        self.assertTrue(hasattr(GeneratedTestCase.test_user_attr, ATTR_NAME))

    def test_decorated_test_methods_are_replaced_with_generated_ones(self):
        class GeneratedTestCase(tcm.TestCase):
            @tcm.values(*range(9), kw=-1)
            def test_few(self, value):
                """Dummy docstring."""
                self.assertIsInstance(value, int)
                return value

            @tcm.values(*range(10))
            def test_many(self, value):
                self.assertIsInstance(value, int)
                return value

        self.assertFalse(hasattr(GeneratedTestCase, 'test_few'))
        self.assertFalse(hasattr(GeneratedTestCase, 'test_many'))

        self.assertFalse(hasattr(GeneratedTestCase.test_few_1, ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_few_9, ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_few_kw, ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_many_01, ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_many_10, ATTR_NAME))

        self.assertEqual(GeneratedTestCase.test_few_2.__doc__, 'Dummy docstring.')
        self.assertIsNone(GeneratedTestCase.test_many_01.__doc__)

        self.assertEqual(GeneratedTestCase.test_few_1.__name__, 'test_few_1')
        self.assertEqual(GeneratedTestCase.test_few_9.__name__, 'test_few_9')
        self.assertEqual(GeneratedTestCase.test_few_kw.__name__, 'test_few_kw')
        self.assertEqual(GeneratedTestCase.test_many_01.__name__, 'test_many_01')
        self.assertEqual(GeneratedTestCase.test_many_10.__name__, 'test_many_10')

        gtc = GeneratedTestCase()

        self.assertEqual(gtc.test_few_1(), 0)
        self.assertEqual(gtc.test_few_9(), 8)
        self.assertEqual(gtc.test_few_kw(), -1)
        self.assertEqual(gtc.test_many_01(), 0)
        self.assertEqual(gtc.test_many_10(), 9)

    def test_values_are_passed_as_is_for_single_arg_test_method(self):
        class GeneratedTestCase(tcm.TestCase):
            @tcm.values(
                tuple(),
                list(),
                dict(),
            )
            def test(self, x):
                self.assertIsInstance(x, (tuple, list, dict))
                return x

        gtc = GeneratedTestCase()

        self.assertTupleEqual(gtc.test_1(), ())
        self.assertListEqual(gtc.test_2(), [])
        self.assertDictEqual(gtc.test_3(), {})

    def test_values_are_unpacked_for_pos_args_test_method(self):
        class GeneratedTestCase(tcm.TestCase):
            @tcm.values(
                ('a', 1),
                ['bb', 2],
                {'x': 'ccc', 'y': 3},
            )
            def test(self, x, y):
                self.assertIsInstance(x, str)
                self.assertIsInstance(y, int)
                return x, y

        gtc = GeneratedTestCase()

        self.assertTupleEqual(gtc.test_1(), ('a', 1))
        self.assertTupleEqual(gtc.test_2(), ('bb', 2))
        self.assertTupleEqual(gtc.test_3(), ('ccc', 3))

    def test_values_are_unpacked_for_star_args_test_method(self):
        class GeneratedTestCase(tcm.TestCase):
            @tcm.values(
                ('a',),
                ['bb', 2],
                ('ccc', 3, None),
            )
            def test(self, *args):
                self.assertIsInstance(args[0], str)
                return args

        gtc = GeneratedTestCase()

        self.assertTupleEqual(gtc.test_1(), ('a',))
        self.assertTupleEqual(gtc.test_2(), ('bb', 2))
        self.assertTupleEqual(gtc.test_3(), ('ccc', 3, None))

    def test_values_are_unpacked_for_keyword_args_test_method(self):
        class GeneratedTestCase(tcm.TestCase):
            @tcm.values(
                {'x': 'a', 'y': 1, 'z': 0},
                {'x': 'bb', 'y': 2},
            )
            def test(self, z='?', **kwargs):
                x = kwargs['x']
                y = kwargs['y']
                self.assertIsInstance(x, str)
                self.assertIsInstance(y, int)
                return x, y, z

        gtc = GeneratedTestCase()

        self.assertTupleEqual(gtc.test_1(), ('a', 1, 0))
        self.assertTupleEqual(gtc.test_2(), ('bb', 2, '?'))

    def test_incompatible_test_method_signature_will_raise_upon_test_run(self):
        class GeneratedTestCase(tcm.TestCase):
            # Each tcm.values item must be a list, a tuple, or a dict because
            # the test method takes two arguments (not a single test argument).
            @tcm.values(
                ['abc'],
            )
            def test_missing(self, x, y):
                pass  # pragma: no cover

            # Each tcm.values item must be a list, a tuple, or a dict because
            # the test method takes no arguments (not a single test argument).
            @tcm.values(
                ['abc'],
            )
            def test_extra(self):
                pass  # pragma: no cover

        gtc = GeneratedTestCase()

        with self.assertRaises(TypeError) as cm:
            gtc.test_missing_1()
        self.assertEqual(
            cm.exception.args[0],
            "test_missing() missing 1 required positional argument: 'y'")

        with self.assertRaises(TypeError) as cm:
            gtc.test_extra_1()
        self.assertEqual(
            cm.exception.args[0],
            'test_extra() takes 1 positional argument but 2 were given')

    def test_incompatible_test_arg_type_will_raise(self):
        with self.assertRaises(tcm.MetaclassException) as cm:
            class _SpoiledTestCase(tcm.TestCase):
                @tcm.values(
                    ('a', 1),
                    2,
                )
                def test(self, x, y):
                    pass    # pragma: no cover

        self.assertEqual(cm.exception.args[0], 'Invalid test arg: 2')

        # Make sure _SpoiledTestCase does not exist.
        self.assertSetEqual(set(locals()), {'self', 'cm'})

    def test_duplicate_test_method_name_will_raise(self):
        with self.assertRaises(tcm.MetaclassException) as cm:
            class _SpoiledTestCase(tcm.TestCase):
                @tcm.values('abc')
                def test(self, value):
                    pass  # pragma: no cover

                def test_1(self):
                    pass  # pragma: no cover

        _source, base = inspect.getsourcelines(
            MetaclassTestCase.test_duplicate_test_method_name_will_raise)
        self.assertEqual(
            cm.exception.args[0],
            f'Duplicate "test_1" attribute at lines {base + 3} and {base + 7}')

        # Make sure _SpoiledTestCase does not exist.
        self.assertSetEqual(set(locals()), {'self', 'cm', '_source', 'base'})
