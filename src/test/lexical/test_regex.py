import unittest

from src.lexical.regex import Regex, get_re_postfix_c_minus
from src.test.lexical.test_case import re_s


class RegexTest(unittest.TestCase):

    def test_get_re_postfix(self):
        for re in re_s:
            re_postfix = Regex.get_re_postfix(re)
            self.assertIsNotNone(re_postfix)
            print(re_postfix)

    def test_get_re_postfix_c_minus(self):
        self.assertTrue(True)
        print(get_re_postfix_c_minus())
