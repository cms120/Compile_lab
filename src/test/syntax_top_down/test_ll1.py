import unittest
from collections import deque

from lexical import lexical_analysis
from syntax_top_down.ll1 import analysis


class LL1Test(unittest.TestCase):
    def test_analysis(self):
        self.assertTrue(True)
        tokens = lexical_analysis.analysis('resource/change_file/源文件/01_var_defn.sy')
        analysis(deque(tokens))
