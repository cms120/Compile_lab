import unittest

from src.syntax import grammar


class GrammarTest(unittest.TestCase):
    def test_get_g_c_minus(self):
        self.assertTrue(True)
        grammar_m = grammar.get_g_c_minus()
        print(grammar_m)
