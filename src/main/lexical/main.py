from FA import get_fa_c_minus
from LexicalAnalysis import LexicalAnaLysis

dfa_c_minus = get_fa_c_minus()  # 获得c--的最小dfa
la = LexicalAnaLysis(dfa_c_minus)
la.analysis()
