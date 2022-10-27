import unittest

from src.lexical.dfa_shan import fa_2_dfa, DFA, get_dfa_minimize_c_minus, \
    get_dfa_c_minus, dfa_minimize
from src.lexical.finite_automation import FA
from src.lexical.graph import graph_dfa_print, graph_fa_print
# from src.lexical.deterministic_finite_automation import dfa_minimize
from src.lexical.regex.regex import Regex
from src.lexical.regex.rules import Rules
from src.test.lexical.test_case import fa_s, dfa_s_shan, re_s


class DFAShanTest(unittest.TestCase):

    def test_fa_2_dfa1(self):  # 直接从fa开始
        self.assertTrue(True)
        fa_list = fa_s[0]
        fa = FA(fa_list[0], fa_list[1], dict(fa_list[2]), fa_list[3], fa_list[4])

        dfa = fa_2_dfa(fa)
        graph_dfa_print(dfa, 'DFA_shan')
        print(dfa)

    def test_fa_2_dfa2(self):  # 从re开始
        self.assertTrue(True)
        re_postfix = Regex.get_re_postfix(re_s[0])
        print(re_postfix)
        rules = Rules.init_by_re_postfix(re_postfix)
        fa = FA.init_by_rules(rules)
        print(fa)
        graph_fa_print(fa, 'FA_shan')
        dfa = fa_2_dfa(fa)
        graph_dfa_print(dfa, 'DFA_shan')
        print(dfa)

    def test_dfa_minimize(self):
        self.assertTrue(True)

        dfa = DFA(dfa_s_shan[0][0],dfa_s_shan[0][1],dfa_s_shan[0][2],dfa_s_shan[0][3],dfa_s_shan[0][4])
        print(dfa_minimize(dfa))

    def test_get_dfa_c_minus(self):
        self.assertTrue(True)
        dfa = get_dfa_c_minus()
        graph_dfa_print(dfa)
        print(dfa)

    def test_get_dfa_minimize_c_minus(self):
        self.assertTrue(True)
        print(get_dfa_c_minus())
        print(get_dfa_minimize_c_minus())


if __name__ == '__main__':
    unittest.main()
