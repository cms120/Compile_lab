import unittest

from src.lexical.finite_automation import FA
from src.lexical.graph import Graph
from src.lexical.regex import Regex
from src.lexical.rules import Rules
from src.test.lexical.test_case import re_s


class GraphTest(unittest.TestCase):
    def test_graph_fa(self):
        self.assertTrue(True)
        for re in re_s:
            print(re)
            re_postfix = Regex.get_re_postfix(re)
            print(re_postfix)
            rules = Rules.init_by_re_postfix(re_postfix)
            # print(rules)
            fa = FA.init_by_rules(rules)
            print(fa)
            Graph.graph_fa_print(fa)
