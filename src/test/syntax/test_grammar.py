import unittest

from src.syntax import grammar


class GrammarTest(unittest.TestCase):
    def test_init_by_string(self):
        self.assertTrue(True)
        print(grammar.Production.init_by_string('Ident -> [a-zA-Z_][a-zA-Z_0-9]*'))

    def test_get_g_c_minus(self):
        self.assertTrue(True)
        grammar_m = grammar.get_g_c_minus_auto()
        print(grammar_m)
