import unittest

from graph import graph_grammar
from syntax.grammar import get_grammar_c_minus, Production
from util import write_file


class GrammarTest(unittest.TestCase):

    def test_init_by_line(self):
        self.assertTrue(True)

        p= Production.init_by_line("4. constDecl -> 'const' bType constDef ( ',' constDef ) * ';';")
        print(p)

    def test_get_grammar_c_minus(self):
        self.assertTrue(True)
        g = get_grammar_c_minus()
        g.check_ll1()

        graph_grammar(g, 'result/grammar/grammar_c_minus')
