import unittest

from src.lexical.deterministic_finite_automation import fa_2_dfa, DFA, dfa_minimize, get_dfa_minimize_c_minus, \
    get_dfa_c_minus
from src.lexical.finite_automation import FA
from src.test.lexical.test_case import fa_s, dfa_s


class DFATest(unittest.TestCase):

    def test_fa_2_dfa(self):
        self.assertTrue(True)
        for k, letters, f, s, z in fa_s:
            fa = FA(k, letters, f, s, z)
            print(fa_2_dfa(fa))

    def test_dfa_minimize(self):
        self.assertTrue(True)
        for k, letters, f, s, z in dfa_s:
            dfa = DFA(k, letters, f, s, z)
            print(dfa_minimize(dfa))

    def test_get_dfa_c_minus(self):
        self.assertTrue(True)
        print(get_dfa_c_minus())

    def test_get_dfa_minimize_c_minus(self):
        self.assertTrue(True)
        print(get_dfa_minimize_c_minus())


if __name__ == '__main__':
    unittest.main()
