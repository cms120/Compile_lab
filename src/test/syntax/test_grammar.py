import unittest

from syntax.grammar import get_grammar_c_minus, Production


class GrammarTest(unittest.TestCase):
    def test_get_grammar_c_minus(self):
        self.assertTrue(True)

        get_grammar_c_minus()

    def test_init_by_line(self):
        self.assertTrue(True)

        for p in Production.init_by_line("4. constDecl -> 'const' bType constDef ( ',' constDef ) * ';';", set()):
            print(p)

    def test_remove_recall(self):
        pass
