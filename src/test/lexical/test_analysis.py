import unittest

from lexical.dfa import get_dfa_minimize_c_minus
from lexical.lexical_analysis import analysis, get_token_list_by_line_dfa


class LATest(unittest.TestCase):

    def test_analysis(self):
        self.assertTrue(True)
        res = analysis('resource/change_file/源文件/03_var_defn.sy')

    def test_get_token_list_by_line_dfa(self):
        self.assertTrue(True)
        line = 'int e = 0, f = 10;'
        get_token_list_by_line_dfa(get_dfa_minimize_c_minus(True), line)
