import unittest

from lexical import TestCases
from src.lexical.FA import *


class FATest(unittest.TestCase):

    def test_get_fa_c_minus(self):
        self.assertTrue(True)
        fa = get_fa_c_minus()
        print(fa)

    def test_fa_s(self):
        for fa in TestCases.fa_s:
            self.assertTrue(fa.k_and_letters())


if __name__ == '__main__':
    unittest.main()
