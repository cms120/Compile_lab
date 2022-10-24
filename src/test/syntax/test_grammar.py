import unittest

from src.syntax.grammar import Production, get_g_c_minus_auto


class GrammarTest(unittest.TestCase):
    def test_init_by_string(self):
        self.assertTrue(True)
        print(Production.init_by_str(''))

    def test_get_g_c_minus(self):
        self.assertTrue(True)
        grammar_m = get_g_c_minus_auto()
        print(grammar_m)
