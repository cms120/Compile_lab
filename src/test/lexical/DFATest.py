import unittest

from lexical import TestCases
from src.lexical.DFA import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_fa_2_dfa(self):
        self.assertTrue(True)
        for fa in TestCases.fa_s:
            print(fa_2_dfa(fa))


if __name__ == '__main__':
    unittest.main()
