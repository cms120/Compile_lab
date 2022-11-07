import os
import unittest

from graph import graph_grammar
from syntax.grammar import get_grammar_c_minus
from syntax_bottom_up.SBUA_shan import get_grammar_c_minus_without_left_recursion, get_grammar_c_minus_without_recall
from util import write_file


class SUBATest(unittest.TestCase):

    def test_get_grammar_c_minus(self):
        self.assertTrue(True)
        g = get_grammar_c_minus()

        file_name = 'g_without_regex'
        graph_grammar(g, file_name)
        write_file(str(g), os.path.join('result/grammar', file_name + '.txt'))

    def test_remove_left_recursion(self):
        self.assertTrue(True)
        g = get_grammar_c_minus_without_left_recursion()

        file_name = 'g_without_left_recursion'
        graph_grammar(g, file_name)
        write_file(str(g), os.path.join('result/grammar', file_name + '.txt'))

    def test_remove_recall(self):
        self.assertTrue(True)
        g = get_grammar_c_minus_without_recall()

        file_name = 'g_without_recall'
        graph_grammar(g, file_name)
        write_file(str(g), os.path.join('result/grammar', file_name + '.txt'))

    def test_first(self):
        self.assertTrue(True)
        g = get_grammar_c_minus_without_left_recursion()
        write_file(str(g), os.path.join('result/grammar', 'g_without_left_recursion' + '.txt'))

        g.set_first()
        write_file(str(g), os.path.join('result/grammar', 'g_without_recall_with_first' + '.txt'))
