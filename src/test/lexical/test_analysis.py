import unittest

from src.lexical.dfa_shan import get_dfa_minimize_c_minus
from src.lexical.lexical_analysis import analysis, get_token_list_by_line_dfa


class LATest(unittest.TestCase):

    def testAnalysis(self):
        self.assertTrue(True)
        res = analysis('src/test/lexical/sy_s/05_var_defn.sy')
        for i in res:
            print(i)

    def test_get_token_list_by_line_dfa(self):
        self.assertTrue(True)
        line = 'int e = 0, f = 10;'
        get_token_list_by_line_dfa(get_dfa_minimize_c_minus(True), line)
