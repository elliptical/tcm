import unittest

import tcm


class TestCase(unittest.TestCase):
    def test_module_docstring_is_present(self):
        self.assertIsNotNone(tcm.__doc__)
