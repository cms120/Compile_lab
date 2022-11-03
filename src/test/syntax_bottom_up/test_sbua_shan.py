import unittest

from src.syntax.grammar import Grammar
from src.syntax_bottom_up.SBUA_shan import remove_left_recursion, remove_recall
from src.util import read_file


class SUBATest(unittest.TestCase):
    def test_remove_left_recursion(self):
        self.assertTrue(True)
        g = Grammar('S')
        g.init_by_lines(read_file('src/test/syntax_bottom_up/test_case/grammar1.txt'))
        remove_left_recursion(g)
        print(g)

    def test_remove_recall(self):
        self.assertTrue(True)
        g = Grammar('S')
        g.init_by_lines(read_file('src/test/syntax_bottom_up/test_case/grammar3.txt'))
        remove_left_recursion(g)
        print(g)

        remove_recall(g)
        print(g)
