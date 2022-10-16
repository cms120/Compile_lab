import unittest

from src.lexical.deterministic_finite_automation import fa_2_dfa
from src.lexical.finite_automation import FA
from src.test.lexical.test_case import fa_s


class MyTestCase(unittest.TestCase):

    def test_fa_2_dfa(self):
        self.assertTrue(True)
        for k, letters, f, s, z in fa_s:
            fa = FA(k, letters, f, s, z)
            print(fa_2_dfa(fa))


if __name__ == '__main__':
    unittest.main()
