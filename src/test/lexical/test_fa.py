import unittest

from lexical.regex.regex import Regex
from src.lexical.finite_automation import *
from src.lexical.finite_automation import FA
from src.test.lexical.test_case import fa_s, re_s


class FATest(unittest.TestCase):

    def test_get_fa_c_minus(self):
        self.assertTrue(True)
        fa = get_fa_c_minus()
        print(fa)

    def test_fa_s(self):
        for k, letters, f, s, z in fa_s:
            fa = FA(k, letters, f, s, z)
            self.assertTrue(fa.k_and_letters())

    def test_init_by_rules(self):
        self.assertTrue(True)
        for re in re_s:
            print(re)
            re_postfix = Regex.get_re_postfix(re)
            print(re_postfix)
            rules = Rules.init_by_re_postfix(re_postfix)
            # print(rules)
            fa = FA.init_by_rules(rules)
            print(fa)


if __name__ == '__main__':
    unittest.main()
