import unittest

import tcm


class MetaclassTestCase(unittest.TestCase):
    # pylint: disable=no-member

    def test_nondecorated_test_methods_keep_their_names(self):
        class GeneratedTestCase(unittest.TestCase, metaclass=tcm.TestCaseMeta):
            def test_no_attr(self):
                pass  # pragma: no cover

            def test_user_attr(self):
                pass  # pragma: no cover

            setattr(test_user_attr, tcm.ATTR_NAME, None)

        self.assertFalse(hasattr(GeneratedTestCase.test_no_attr, tcm.ATTR_NAME))
        self.assertTrue(hasattr(GeneratedTestCase.test_user_attr, tcm.ATTR_NAME))

    def test_decorated_test_methods_are_replaced_with_generated_ones(self):
        class GeneratedTestCase(unittest.TestCase, metaclass=tcm.TestCaseMeta):
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

        self.assertFalse(hasattr(GeneratedTestCase.test_few_1, tcm.ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_few_9, tcm.ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_few_kw, tcm.ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_many_01, tcm.ATTR_NAME))
        self.assertFalse(hasattr(GeneratedTestCase.test_many_10, tcm.ATTR_NAME))

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

    def test_incompatible_test_method_signature_will_raise_upon_test_run(self):
        class GeneratedTestCase(unittest.TestCase, metaclass=tcm.TestCaseMeta):
            @tcm.values('abc')
            def test_missing(self, x, y):
                pass  # pragma: no cover

            @tcm.values('abc')
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

    def test_duplicate_test_method_name_will_raise(self):
        with self.assertRaises(tcm.MetaclassException) as cm:
            class _SpoiledTestCase(unittest.TestCase, metaclass=tcm.TestCaseMeta):
                @tcm.values('abc')
                def test(self, value):
                    pass  # pragma: no cover

                def test_1(self):
                    pass  # pragma: no cover

        self.assertEqual(cm.exception.args[0], 'The "test_1" attribute already exists')
        self.assertSetEqual(set(locals()), {'self', 'cm'})  # _SpoiledTestCase not created
