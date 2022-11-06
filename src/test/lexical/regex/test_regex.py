import unittest

from lexical.regex.regex import Regex, get_re_postfix_c_minus, re_c_minus
from test.lexical.test_case import re_s


class RegexTest(unittest.TestCase):

    def test_get_re_postfix(self):
        for re in re_s:
            re_postfix = Regex.get_re_postfix(re)
            self.assertIsNotNone(re_postfix)
            print(re_postfix)

    def test_get_re_postfix_c_minus(self):
        print(re_c_minus)
        self.assertTrue(True)
        print(get_re_postfix_c_minus())
