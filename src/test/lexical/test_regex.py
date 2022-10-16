import unittest

from src.test.lexical.test_case import re_s
from src.lexical.finite_automation import FA
from src.lexical.regex import Regex




class RegexTest(unittest.TestCase):
    def test_get_f_by_regex(self):
        self.assertTrue(True)
        for re in re_s:
            re_postfix = Regex.get_re_postfix(re)
            print(re_postfix)
            print(FA.get_f_by_re_postfix(re_postfix))

    def test_get_re_postfix(self):
        for re in re_s:
            re_postfix = Regex.get_re_postfix(re)
            self.assertIsNotNone(re_postfix)
            print(re_postfix)
