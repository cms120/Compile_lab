import unittest

from lexical import lexical_analysis
from lexical.token import tokens_to_deque
from syntax_top_down.ll1 import analysis


class LL1Test(unittest.TestCase):
    def test_analysis(self):
        self.assertTrue(True)
        tokens = lexical_analysis.analysis('resource/change_file/源文件/01_var_defn.sy')
        analysis(tokens_to_deque(tokens))
