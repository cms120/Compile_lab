from src.lexical.FA import FA


class DFA(FA):

    @classmethod
    def init_by_fa(cls, fa: FA):  # 根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))




def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    pass  # TODO


def dfa_minimize(dfa) -> DFA:  # DFA最小化
    pass  # TODO
