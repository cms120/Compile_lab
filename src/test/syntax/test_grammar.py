import unittest

from src.syntax.grammar import Grammar,get_grammar_c_minus


class GrammarTest(unittest.TestCase):
    def test_init_c_minus(self):
        self.assertTrue(True)

        print(get_grammar_c_minus())
