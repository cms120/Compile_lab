import unittest

from src.lexical.finite_automation import FA

re_s = [
    'a.b.c.d',
    '(a|b)*',
    '(a|b).c',
    ''
]


class RegexTest(unittest.TestCase):
    def test_get_f_by_regex(self):
        self.assertTrue(True)
        for re in re_s:
            print(FA.get_f_by_regex(re))
