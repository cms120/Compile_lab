import unittest

from src.lexical.finite_automation import FA, get_fa_c_minus
from src.lexical.graph import graph_fa_print
from src.lexical.regex import Regex
from src.lexical.rules import Rules
from src.test.lexical.test_case import re_s


class GraphTest(unittest.TestCase):
    def test_graph_fa_c_minus(self):
        self.assertTrue(True)
        graph_fa_print(get_fa_c_minus())

    def test_graph_fa(self):
        self.assertTrue(True)

        print(re_s[0])
        re_postfix = Regex.get_re_postfix(re_s[0])
        print(re_postfix)
        rules = Rules.init_by_re_postfix(re_postfix)
        # print(rules)
        fa = FA.init_by_rules(rules)
        print(fa)
        graph_fa_print(fa)
