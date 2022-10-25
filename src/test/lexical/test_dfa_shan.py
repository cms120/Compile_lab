import unittest

from src.lexical.dfa_shan import fa_2_dfa, DFA, dfa_minimize, get_dfa_minimize_c_minus, \
    get_dfa_c_minus
from src.lexical.finite_automation import FA
from src.lexical.graph import graph_dfa_print
from src.test.lexical.test_case import fa_s, dfa_s


class DFAShanTest(unittest.TestCase):

    def test_fa_2_dfa(self):
        self.assertTrue(True)
        fa_list = fa_s[0]
        fa = FA(fa_list[0], fa_list[1], dict(fa_list[2]), fa_list[3], fa_list[4])

        dfa = fa_2_dfa(fa)
        graph_dfa_print(dfa, 'DFA_shan')
        print(dfa)

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
