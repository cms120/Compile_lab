import unittest

from src.lexical.finite_automation import *
from src.lexical.finite_automation import FA
from src.test.lexical.test_case import fa_s


class FATest(unittest.TestCase):

    def test_get_fa_c_minus(self):
        self.assertTrue(True)
        fa = get_fa_c_minus()
        print(fa)

    def test_fa_s(self):
        for k, letters, f, s, z in fa_s:
            fa = FA(k, letters, f, s, z)
            self.assertTrue(fa.k_and_letters())


if __name__ == '__main__':
    unittest.main()
