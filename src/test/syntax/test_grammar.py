import unittest

from src.syntax.grammar import Grammar


class GrammarTest(unittest.TestCase):
    def test_init_c_minus(self):
        self.assertTrue(True)
        g = Grammar()
        g.init_c_minus()
        print(g)
