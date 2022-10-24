import unittest

from src.lexical.regex import Regex
from src.lexical.rules import Rules, get_rules_c_minus
from src.test.lexical.test_case import re_s


class RulesTest(unittest.TestCase):
    def test_init_by_re_postfix(self):
        self.assertTrue(True)
        # re_s.append(_INT+'|'+_IDN+'|'+'+|-|\\*|/|%|=|>|<|!|&|:|;|{|}|\\(|\\)|,| |\n|\t')
        for re in re_s:
            re_postfix = Regex.get_re_postfix(re)
            print(re_postfix)
            rules = Rules.init_by_re_postfix(re_postfix)
            print(rules)

    def test_get_rules_c_minus(self):
        self.assertTrue(True)
        print(get_rules_c_minus())
