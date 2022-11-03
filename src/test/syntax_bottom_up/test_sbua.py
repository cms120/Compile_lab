import unittest

from src.syntax.grammar import get_grammar_c_minus
from src.syntax_bottom_up.SBUA_shan import remove_left_recursion


class SUBATest(unittest.TestCase):
    def test_remove_left_recursion(self):
        self.assertTrue(True)
        g = get_grammar_c_minus()
        remove_left_recursion(g)
        print(g)
