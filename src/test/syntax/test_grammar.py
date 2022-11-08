import unittest

from graph import graph_grammar
from syntax.grammar import get_grammar_c_minus, Production
from util import write_file


class GrammarTest(unittest.TestCase):

    def test_init_by_line(self):
        self.assertTrue(True)

        for p in Production.init_by_line("4. constDecl -> 'const' bType constDef ( ',' constDef ) * ';';"):
            print(p)

    def test_remove_recall(self):
        pass

    def test_get_grammar_c_minus(self):
        self.assertTrue(True)
        g = get_grammar_c_minus()
        g.set_first()
        g.set_follow()
        g.check_first()

        file_name = 'result/grammar/grammar_c_minus'
        graph_grammar(g, file_name)
        write_file(str(g), file_name + '.txt')
