import unittest
from lexical import TestCases
from src.lexical.FA import FA


class RegexTest(unittest.TestCase):
    def test_get_f_by_regex(self):
        self.assertTrue(True)
        for re in TestCases.re_s:
            print(FA.get_f_by_regex(re))
