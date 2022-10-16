import unittest

from src.lexical.finite_automation import FA
from src.lexical.regex import Regex

re_s = [
    '',
    'a.b.c.d',
    '(a|b)*',
    '(a|b).c'
]


class RegexTest(unittest.TestCase):
    def test_get_f_by_regex(self):
        self.assertTrue(True)
        for re in re_s:
            print(FA.get_f_by_regex(
                Regex.get_re_postfix(re)))

    def test_get_re_postfix(self):
        for re in re_s:
            re_postfix = Regex.get_re_postfix(re)
            self.assertIsNotNone(re_postfix)
            print(re_postfix)
