from src.lexical.finite_automation import get_fa_c_minus
from src.lexical.lexical_analysis import LexicalAnaLysis
from src.lexical.deterministic_finite_automation import DFA

dfa_c_minus = DFA.init_by_fa(get_fa_c_minus())   # 获得c--的最小dfa
la = LexicalAnaLysis(dfa_c_minus)
la.analysis()
